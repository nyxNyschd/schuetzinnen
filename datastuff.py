
meineListe = ['The competition concerns the delivery of asphalt works on municipal roads, streets, foot and cycle paths, pavements, squares, parking places, some private roads and any selected new installations that are operated and maintained by the individual municipalities.The annual value of the procurement is estimated to be: 15 000 000 NOK-30 000 000 NOK excluding VAT per year. The value is an estimate and, thus, not binding. See the tender documentation for further information.', 'The establishment of a provisional cable installations at Mosseporten transformation station.', 'Construction of a power line route in Moss.', 'Building and ground work in Mosseporten transformer station.', 'The contract includes all work that needs to be carried out with an excavator or similar machinery and associated necessary works, in connection with archaeological records, surveys and excavations.', 'The contract includes all work that needs to be carried out with an excavator or similar machinery and associated necessary works, in connection with archaeological records, surveys and excavations.', 'ØRIK invites tenderers to an open tender competition for the delivery of water meters for the municipalities of: Eidsvoll, Gjerdrum, Hurdal, Nannestad, Nes and Ullensaker.See the requirement specifications for further information.']

def all_values_containing_substring(substring):
    gotIt = []
    for i, s in enumerate(meineListe):
        if substring in s:
              gotIt.append(meineListe[i])
    return gotIt


