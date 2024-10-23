def get_values(*names):
    import json
    _all_values = json.loads("""{"p300_multi_mount":"right","number_of_samples":96,"volume_of_beads":27,"first_bead_incubation_time_in_minutes":8,"second_bead_incubation_time_in_minutes":2,"etoh_inc":5,"drying_time_in_minutes":1.5,"vol_etoh":100,"mix_etoh":false,"volume_EB_in_ul":30,"elution_inc":2,"volume_final_elution_in_ul":27,"park_tips":true,"tip_track":false,"drop_threshold":200}""")
    return [_all_values[n] for n in names]

import math
import os
import json
from opentrons.types import Point

metadata = {
#    'protocolName': '32 Sample Cleanup Round 1', # Heavily based on this
    'protocolName': '96 Sample Bear Looping Cleanup',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.9'
}

MAG_HEIGHT = 6.8

def run(ctx):
    ### Common Part:
    # Load data:
    [p300_multi_mount, number_of_samples, volume_of_beads,
     first_bead_incubation_time_in_minutes, second_bead_incubation_time_in_minutes, etoh_inc, drying_time_in_minutes,
     vol_etoh, mix_etoh, volume_EB_in_ul, elution_inc,
     volume_final_elution_in_ul, park_tips, tip_track,
     drop_threshold] = get_values(  # noqa: F821
        'p300_multi_mount', 'number_of_samples', 'volume_of_beads',
        'first_bead_incubation_time_in_minutes', 'second_bead_incubation_time_in_minutes', 'etoh_inc',
        'drying_time_in_minutes', 'vol_etoh', 'mix_etoh', 'volume_EB_in_ul',
        'elution_inc', 'volume_final_elution_in_ul', 'park_tips', 'tip_track',
        'drop_threshold')
    
    # check
    if number_of_samples > 96 or number_of_samples < 1:
        raise Exception('Invalid number of samples.')

    # Calculate number of columns:
    num_cols = math.ceil(number_of_samples/8)

    # load labware
    magdeck = ctx.load_module('magnetic module gen2', '1')
    mag_plate = magdeck.load_labware(
        'nest_96_wellplate_100ul_pcr_full_skirt', 'magnetic plate')
    elution_plate = ctx.load_labware(
        'nest_96_wellplate_100ul_pcr_full_skirt', '2', 'elution plate')
    tips300 = [
        ctx.load_labware('opentrons_96_filtertiprack_200ul', slot)
        for slot in ['6', '8', '9', '10', '11', '3']]
    if park_tips:
        rack = ctx.load_labware(
            'opentrons_96_filtertiprack_200ul', '5', 'tiprack for parking')
        parking_spots = rack.rows()[0][:num_cols]
    else:
        rack = ctx.load_labware(
            'opentrons_96_filtertiprack_200ul', '5', '200µl filtertiprack')
        parking_spots = [None for none in range(12)]
    tips300.insert(0, rack)

    deep96 = ctx.load_labware('nest_12_reservoir_15ml', '7',
                              'reagent deepwell plate')
    waste_plate = ctx.load_labware('nest_12_reservoir_15ml', '4',
                                   'waste deepwell plate')

    # sample setup
    mag_samples = mag_plate.rows()[0][:num_cols]
    elution_samples = elution_plate.rows()[0][:num_cols]
    waste = [chan.top(-5) for chan in waste_plate.rows()[0][:num_cols]]
    num_drying_sets = math.ceil(num_cols/4)  # process 4 columns at a time
    drying_sets = [
        mag_samples[i*4:i*4+4] if i < num_drying_sets - 1
        else mag_samples[i*4:]
        for i in range(num_drying_sets)]
    # parking_sets contains a list of lists of columns:
    parking_sets = [
        parking_spots[i*4:i*4+4] if i < num_drying_sets - 1
        else parking_spots[i*4:]
        for i in range(num_drying_sets)]
    waste_sets = [
        waste[i*4:i*4+4] if i < num_drying_sets - 1
        else waste[i*4:]
        for i in range(num_drying_sets)]

    # reagents
    beads = deep96.rows()[0][0]
    etoh = deep96.rows()[0][1]
    eb_buff = deep96.rows()[0][2]

    # pipettes
    m300 = ctx.load_instrument(
        'p300_multi_gen2', mount=p300_multi_mount, tip_racks=tips300)
    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 200

    tip_log = {val: {} for val in ctx.loaded_instruments.values()}
    folder_path = '/data/bead_cleanup'
    tip_file_path = folder_path + '/tip_log.json'
    if tip_track and not ctx.is_simulating():
        if os.path.isfile(tip_file_path):
            with open(tip_file_path) as json_file:
                data = json.load(json_file)
                for pip in tip_log:
                    if pip.name in data:
                        tip_log[pip]['count'] = data[pip.name]
                    else:
                        tip_log[pip]['count'] = 0
        else:
            for pip in tip_log:
                tip_log[pip]['count'] = 0
    else:
        for pip in tip_log:
            tip_log[pip]['count'] = 0

    for pip in tip_log:
        if pip.type == 'multi':
            tip_log[pip]['tips'] = [tip for rack in pip.tip_racks
                                    for tip in rack.rows()[0]]
        else:
            tip_log[pip]['tips'] = [tip for rack in pip.tip_racks
                                    for tip in rack.wells()]
        tip_log[pip]['max'] = len(tip_log[pip]['tips'])

    def pick_up(pip, loc=None):
        if tip_log[pip]['count'] == tip_log[pip]['max'] and not loc:
            ctx.pause('Replace ' + str(pip.max_volume) + 'µl tipracks before \
    resuming.')
            pip.reset_tipracks()
            tip_log[pip]['count'] = 0
        if loc:
            pip.pick_up_tip(loc)
            return loc
        else:
            loc = tip_log[pip]['tips'][tip_log[pip]['count']]
            pip.pick_up_tip(loc)
            tip_log[pip]['count'] += 1
            return loc

    switch = True
    drop_count = 0
    # number of tips trash will accommodate before prompting user to empty

    def drop(pip, loc=None):
        nonlocal switch
        nonlocal drop_count
        if not loc:
            if pip.type == 'multi':
                drop_count += 8
            else:
                drop_count += 1
            if drop_count >= drop_threshold:
                ctx.home()
                ctx.pause('Please empty tips from waste before resuming.')
                drop_count = 0
            side = 30 if switch else -18
            drop_loc = ctx.loaded_labwares[12].wells()[0].top().move(
                Point(x=side))
            pip.drop_tip(drop_loc)
            switch = not switch
        else:
            pip.drop_tip(loc)

    ### Repeated part:
    
    num_drying_sets = 1 # test to change from 3 since we are splitting on our own
    
    # Function for running a given set of columns:
    def run_columns(mag_samples, parking_spots, elution_samples, waste, drying_sets, waste_sets): 
        # mix beads
        ctx.max_speeds['A'] = 50
        ctx.max_speeds['Z'] = 50
        # transfer beads and mix samples
        for m, p in zip(mag_samples, parking_spots):
            pick_up(m300)
            m300.mix(5, volume_of_beads, beads.bottom(3))
            m300.blow_out(beads.top(-5))
            m300.transfer(volume_of_beads, beads, m.bottom(3), new_tip='never')
            m300.blow_out(m.top(-2))
            for _ in range(10):
                m300.aspirate(volume_of_beads+25, m.bottom(3))
                m300.dispense(volume_of_beads+25, m.center())
            m300.blow_out(m.top(-2))
            drop(m300, p)
        ctx.max_speeds['A'] = 125
        ctx.max_speeds['Z'] = 125

        # incubation
        ctx.delay(minutes=first_bead_incubation_time_in_minutes, msg='Incubating off \
    magnet for ' + str(first_bead_incubation_time_in_minutes) + ' minutes.')
        magdeck.engage(height=MAG_HEIGHT)
        ctx.delay(minutes=etoh_inc, msg='Incubating \
    on magnet for ' + str(etoh_inc) + ' minutes.')

        # remove supernatant
        for m, p, w in zip(mag_samples, parking_spots, waste):
            pick_up(m300, p)
            m300.aspirate(54, m.bottom(1.5))
            m300.air_gap(20)
            m300.dispense(74, w, rate=0.7)
            m300.blow_out(w)
            m300.air_gap(20)
            drop(m300, p)

        # 2x EtOH washes
        etoh_loc = None
        for wash in range(2):
            if mix_etoh:
                magdeck.disengage()

            # transfer EtOH
            if wash == 0:
                etoh_loc = pick_up(m300)
            else:
                pick_up(m300, etoh_loc)

            m300.distribute(vol_etoh, etoh, [m.top(2) for m in mag_samples],
                            blow_out=True, blowout_location='source well',
                            new_tip='never')
            if wash == 0:
                drop(m300, etoh_loc)
            else:
                drop(m300)
            if mix_etoh:
                for m, p in zip(mag_samples, parking_spots):
                    pick_up(m300, p)
                    m300.mix(10, vol_etoh*0.8, m)
                    m300.blow_out(m.top())
                    drop(m300, p)

            if mix_etoh:
                magdeck.engage(height=MAG_HEIGHT)
                ctx.delay(minutes=etoh_inc, msg='Incubating on magnet for \
    ' + str(etoh_inc) + ' minutes.')

            # remove supernatant
            if wash == 0:
                for m, p, w in zip(mag_samples, parking_spots, waste):
                    if mix_etoh:
                        pick_up(m300, p)
                    else:
                        if not m300.has_tip:
                            pick_up(m300, p)
                    m300.aspirate(vol_etoh, m.bottom(1.5))
                    m300.air_gap(20)
                    m300.dispense(vol_etoh+20, w, rate=0.7)
                    m300.blow_out(w)
                    m300.air_gap(20)
                    drop(m300, p)
            else:
                for m, p, w in zip(mag_samples, parking_spots, waste):
                    if mix_etoh:
                        pick_up(m300, p)
                    else:
                        if not m300.has_tip:
                            pick_up(m300, p)
                    m300.aspirate(vol_etoh, m.bottom(1.5))
                    m300.air_gap(20)
                    m300.dispense(vol_etoh + 20, w, rate=0.7)
                    m300.air_gap(20)
                    drop(m300, p)

                # Columns get looped in sets of 4:
                eb_tip = None
                for set_ind, (sample_set, parking_set, waste_set) in enumerate(
                        zip(drying_sets, parking_sets, waste_sets)):
                    print("set_ind:", set_ind)
                    print("sample_set:", sample_set)
               

                    ctx.delay(
                        minutes=drying_time_in_minutes, msg='Drying for \
    ' + str(drying_time_in_minutes) + ' minutes.')

                    # transfer EB buffer
                    if set_ind == 0:
                        eb_tip = pick_up(m300)
                    else:
                        pick_up(m300, eb_tip)

                    # custom distribution
                    col_per_asp = math.floor(180/volume_EB_in_ul)
                    num_asp = math.ceil(len(sample_set)/col_per_asp)
                    dist_sets = [
                        sample_set[i*col_per_asp:i*col_per_asp+col_per_asp]
                        if i < num_asp - 1
                        else sample_set[i*col_per_asp:]
                        for i in range(num_asp)]
                    for dist_set in dist_sets:
                        m300.dispense(m300.current_volume, eb_buff.top())
                        m300.distribute(volume_EB_in_ul, eb_buff,
                                        [m.top(2) for m in dist_set],
                                        blow_out=True,
                                        blowout_location='source well',
                                        new_tip='never')
                        m300.air_gap(20)
                    if set_ind == len(sample_set) - 1:
                        drop(m300)
                    else:
                        drop(m300, eb_tip)

        magdeck.disengage()

        # mix samples
        for m in mag_samples:
            pick_up(m300)
            m300.mix(10, 0.8*volume_EB_in_ul, m)
            m300.blow_out(m.top())
            drop(m300)

        ctx.delay(minutes=second_bead_incubation_time_in_minutes, msg='Incubating off \
    magnet for ' + str(second_bead_incubation_time_in_minutes) + ' minutes.')
        magdeck.engage(height=MAG_HEIGHT)
        ctx.delay(minutes=elution_inc, msg='Incubating on magnet for \
    ' + str(elution_inc) + ' minutes.')

        # transfer supernatant to new PCR plate
        m300.flow_rate.aspirate = 20
        for i, (m, e, p) in enumerate(
                zip(mag_samples, elution_samples, parking_spots)):
            pick_up(m300)
            side = -1 if i % 2 == 0 else 1
            m300.transfer(volume_final_elution_in_ul,
                          m.bottom().move(Point(x=side*2.0, z=1.5)), e,
                          new_tip='never')
            m300.blow_out(e.top(-2))
            drop(m300)

        magdeck.disengage()

        # track final used tip
        if tip_track and not ctx.is_simulating():
            if not os.path.isdir(folder_path):
                os.mkdir(folder_path)
            data = {pip.name: tip_log[pip]['count'] for pip in tip_log}
            with open(tip_file_path, 'w') as outfile:
                json.dump(data, outfile)

    counter = 0
    for i in range(0, len(mag_samples), 4):
        print("### RUNNING COLUMN SET ", counter)
        # mag_samples: an object containing columns by name, here we split into chunks of four
        # elution_samples: -"-
        # waste: -"-
        # num_drying_sets: number of sets of drying cols, 3 if 96 samples but we set it to 1 above since we run 4 cols at a time
        # drying_sets = a list of lists of sets of columns [[col1, col2], [col3, col4]], we take one internal list at a time
        # waste_sets = -"- (just like drying sets this might get weird with fewer samples than 96)
        run_columns(mag_samples[i:i + 4], parking_spots[i:i + 4], elution_samples[i:i + 4], waste[i:i + 4], [drying_sets[counter]], [waste_sets[counter]])
        counter = counter + 1
