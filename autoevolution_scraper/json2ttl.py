import json
import re


def populate_brands(data):
    with open("auto_evolution.ttl", "a") as auto_evolution:
        for brand in data:
            nameBrand = brand['nameBrand']
            imageBrand = brand['imageBrand']
            urlBrand = brand['urlBrand']
            historyBrand = brand['infoBrand']['history'].replace('\n\r\n', '')
            historyBrand = brand['infoBrand']['history'].replace('\n', '')
            productionModelsBrand = brand['infoBrand']['productionModels']
            discontinuedModelsBrand = brand['infoBrand']['discontinuedModels']
            historyBrand = historyBrand.replace('"', '')
            brand_aux = '''
###  http://www.semanticweb.org/rafaelsilva/ontologies/2020/auto-evolution#{0}
:{1} rdf:type owl:NamedIndividual ,
        :Brand ;
    :brandDiscontinuedModels "{2}"^^xsd:string ;
    :brandProductionModels "{3}"^^xsd:string ;
    :historyBrand "{4}";
    :imageBrand "{5}"^^xsd:string ;
    :nameBrand "{6}"^^xsd:string ;
    :urlBrand "{7}"^^xsd:string .
    '''.format(nameBrand,nameBrand,discontinuedModelsBrand,productionModelsBrand,historyBrand,imageBrand,nameBrand,urlBrand)
            auto_evolution.write(brand_aux)
            auto_evolution.write('\n')
        auto_evolution.close()

def populate_classes(data):
    with open("auto_evolution.ttl", "a") as auto_evolution:
        for classe in data:
            classe_aux = '''
###  http://www.semanticweb.org/rafaelsilva/ontologies/2020/auto-evolution#{0}
:{0} rdf:type owl:NamedIndividual ,
               :Classes ;
      :className "{0}"^^xsd:string .
'''.format(classe['class'])
            auto_evolution.write(classe_aux)
            auto_evolution.write('\n')
        auto_evolution.close()

def populate_fuels(data):
    with open("auto_evolution.ttl", "a") as auto_evolution:
        for fuel in data:
            fuel_aux = '''
###  http://www.semanticweb.org/rafaelsilva/ontologies/2020/auto-evolution#{0}
:{0} rdf:type owl:NamedIndividual ,
                   :Fuels ;
          :nameFuel "{0}"^^xsd:string .
'''.format(fuel['fuel'])
            auto_evolution.write(fuel_aux)
            auto_evolution.write('\n')
        auto_evolution.close()

def populate_model(data):
    with open("auto_evolution.ttl", "a") as auto_evolution:
        for model in data:
            brand_name = model['nameBrand']
            model_name = model['name']
            if model['class']:
                model_class = model['class']
            fuels_aux = ''
            for fuel in model['fuels']:
                if fuel:
                    fuel = re.sub(r'-|\s+', '_', fuel)
                    fuels_aux += ':' + fuel
                    fuels_aux += ' , '
                else:
                    fuel = 'None'
                    fuels_aux += ':' + fuel
                    fuels_aux += ' , '
            fuels_aux = fuels_aux[:-2]
            fuels_aux += ';'
            model_img = model['img']
            modelYears = model['modelYears']
            model_nrGenerations = model['nrGenerations']
            model_url = model['url']
            model_aux = '''
###  http://www.semanticweb.org/rafaelsilva/ontologies/2020/auto-evolution#{0}
:{0} rdf:type owl:NamedIndividual ,
            :Models ;
    :pertenceClass :{1} ;
    :pertenceMarca :{2} ;
    :usaCombustivel {3}
    :imgModel "{4}"^^xsd:string ;
    :modelYears "{5}"^^xsd:string ;
    :nameModel "{0}"^^xsd:string ;
    :nrGenerationsModel "{6}"^^xsd:string ;
    :urlModel "{7}"^^xsd:string .
'''.format(model_name,model_class,brand_name,fuels_aux,model_img,modelYears,model_nrGenerations,model_url)
            auto_evolution.write(model_aux)
            auto_evolution.write('\n')
        auto_evolution.close()

def populate_version(data):
    with open("auto_evolution.ttl", "a") as auto_evolution:
        for model in data:
            version = model['version']
            modelName = model['name']
            version['version_name'] = re.sub(r'-|/|&|{|}|:', '_', version['version_name'])
            version['version_name'] = re.sub(r'!|,|\s+|%', '', version['version_name'])
            version['version_name'] = version['version_name'].replace('.','_')
            version['version_name'] = version['version_name'].replace('(','_')
            version['version_name'] = version['version_name'].replace(')','_')
            version['version_name'] = version['version_name'].replace('+','')
            version_name = version['version_name']
            gallery = version['gallery']
            version_url = version['version_url']
            years = version['years']
            info = version['info']
            segment = 'None'
            if 'segment' in info:
                segment = info['segment']
            body_style = 'None'
            if 'bodyStyle' in info:
                body_style = info['bodyStyle']
            descriptionVersion = 'None'
            if 'description' in info:
                descriptionVersion = info['description']
            introVersion = 'None'
            if 'intro' in info:
                introVersion = info['intro']
            specs = parse_specs(info)
            version_aux = '''
###  http://www.semanticweb.org/rafaelsilva/ontologies/2020/auto-evolution#{0}
:{0} rdf:type owl:NamedIndividual ,
            :Versions ;
            :pertenceModelo :{1} ;
            :bodyStyleVersion "{2}"^^xsd:string ;
            :galleryVersion "{3}"^^xsd:string ;
            :segmentVersion "{4}"^^xsd:string ;
            :versionName "{0}"^^xsd:string ;
            :versionUrl "{5}"^^xsd:string ;
            :yearsVersion "{6}"^^xsd:string ;
            :descriptionVersion "{7}"^^xsd:string ;
            :introVersion "{8}"^^xsd:string ;
            :specs "{9}"^^xsd:string .
        '''.format(version_name,modelName,body_style,gallery,segment,version_url,years,descriptionVersion,introVersion,specs)
            auto_evolution.write(version_aux)
            auto_evolution.write('\n')
        auto_evolution.close()

def parse_specs(info):
    enginespecs = '-> Engine Specs: '
    if 'enginespecs' in info:
        engine = info['enginespecs']
        if engine != {}:
            if 'cylinders' in engine:
                enginespecs += 'cylinders: ' + engine['cylinders'] + ' '
            if 'displacement' in engine:
                enginespecs += 'displacement: ' + engine['displacement'] + ' '
            if 'power' in engine:
                for aux in engine['power']:
                    enginespecs += 'power: ' + aux + ' '
            if 'torque' in engine:
                for aux in engine['torque']:
                    enginespecs += 'torque: ' + aux + ' '
            if 'fuel-system' in engine:
                enginespecs += 'fuel-system: ' + engine['fuel-system'] + ' '
            if 'fuel' in engine:
                enginespecs += 'fuel: ' + engine['fuel'] + ' '
            if 'fuel-capacity' in engine:
                enginespecs += 'fuel-capacity: ' + engine['fuel-capacity'] + ' '
        else: 
            enginespecs += 'None' + ' '
    else: 
        enginespecs += 'None' + ''
    
    performancespecs = 'Performance Specs: '
    if 'performancespecs' in info:
        performance = info['performancespecs']
        if performance != {}:
            if 'top-speed' in performance:
                performancespecs += 'top-speed: ' + performance['top-speed'] +' '
            if 'acceleration-0-62-mph-(0-100-kph)' in performance:
                performancespecs += 'acceleration-0-62-mph-(0-100-kph): ' + performance['acceleration-0-62-mph-(0-100-kph)'] +' '
        else:
            performancespecs += 'None' + ' '
    else:
        performancespecs += 'None' + ' '
    
    transmissionspecs = '-> Transmission Specs: '
    if 'transmissionspecs' in info:
        transmission = info['transmissionspecs']
        if transmission != {}:
            if 'drive-type' in transmission:
                transmissionspecs += 'drive-type: ' + transmission['drive-type'] +' '
            if 'gearbox' in transmission:
                transmissionspecs += 'gearbox: ' + transmission['gearbox'] +' '
        else:
            transmissionspecs += 'None' + ' '
    else:
        transmissionspecs += 'None' + ' '
    
    brakesspecs = '-> Brakes Specs: '
    if 'brakesspecs' in info:
        brakes = info['brakesspecs']
        if brakes != {}:
            if 'front' in brakes:
                brakesspecs += 'front: ' + brakes['front'] + ' '
            if 'rear' in brakes:
                brakesspecs += 'rear: ' + brakes['rear'] + ' '
        else:
            brakesspecs += 'None' + ' '
    else:
        brakesspecs += 'None' + ' '

    tiresspecs = '-> Tires Specs: '
    if 'tiresspecs' in info:
        tires = info['tiresspecs']
        if tires != {}:
            if 'tire-size' in tires:
                tiresspecs += 'tire-size: ' + tires['tire-size'] +' '
        else:
            tiresspecs += 'None' + ' '
    else:
        tiresspecs += 'None' + ' '

    dimensions = '-> Dimensions: '
    if 'dimensions' in info:
        dim = info['dimensions']
        if dim != {}:
            if 'length' in dim:
                dimensions += 'length: ' + dim['length'] +' '
            if 'width' in dim:
                dimensions += 'width: ' + dim['width'] +' '
            if 'height' in dim:
                dimensions += 'height: ' + dim['height'] +' '
            if 'front/rear-track' in dim:
                dimensions += 'front/rear-track: ' + dim['front/rear-track'] +' '
            if 'wheelbase' in dim:
                dimensions += 'wheelbase: ' + dim['wheelbase'] +' '
            if 'ground-clearance' in dim:
                dimensions += 'ground-clearance: ' + dim['ground-clearance'] +' '
            if 'cargo-volume' in dim:
                dimensions += 'cargo-volume: ' + dim['cargo-volume'] +' '
            if 'aerodynamics-(cd)' in dim:
                dimensions += 'aerodynamics-(cd): ' + dim['aerodynamics-(cd)'] +' '
        else:
            dimensions += 'None' + ' '
    else:
        dimensions += 'None' + ' '

    weightspecs = '-> Weight Specs: '
    if 'weightspecs' in info:
        weight = info['weightspecs']
        if weight != {}:
            if 'unladen-weight' in weight:
                weightspecs += 'unladen-weight: ' + weight['unladen-weight'] +' '
            if 'gross-weight-limit' in weight:
                weightspecs += 'gross-weight-limit: ' + weight['gross-weight-limit'] +' '
        else:
            weightspecs += 'None' + ' '
    else:
        weightspecs += 'None' + ' '

    fueleconomy = '-> Fuel Economy: '
    if 'fueleconomy' in info:
        fueleco = info['fueleconomy']
        if fueleco != {}:
            if 'city' in fueleco:
                fueleconomy += 'city: ' + fueleco['city'] + ' '
            if 'highway' in fueleco:
                fueleconomy += 'highway: ' + fueleco['highway'] + ' '
            if 'combined' in fueleco:
                fueleconomy += 'combined: ' + fueleco['combined'] + ' ' 
            if 'co2-emissions' in fueleco:
                fueleconomy += 'co2-emissions: ' + fueleco['co2-emissions'] + ' '

        else:
            fueleconomy += 'None' + ' '
    else:
        fueleconomy += 'None' + ' '

    notes = '-> Notes: '
    if 'notes' in info:
        note = info['notes']
        if note != {}:
            if 'notice' in note:
                for aux in note['notice']:
                    if aux != '':
                        notes += 'note: ' + aux + ' '
        else:
            notes += 'None' + ' '
    else:
        notes += 'None' + ' '

    final_specs = '''{0} {1} {2} {3} {4} {5} {6} {7} {8}'''.format(enginespecs, performancespecs, transmissionspecs, brakesspecs, tiresspecs, dimensions, weightspecs, fueleconomy, notes)
    
    return final_specs 


with open('autoevolution.txt') as data_auto_evolution:
    data_auto = json.load(data_auto_evolution)
    brands = list()
    classes = list()
    models = list()
    fuels = list()
    versions = list()
    for row in data_auto:
        brand = row['brand']
        brand['nameBrand'] = re.sub(r'-|/|&|{|}', '_',  brand['nameBrand'])
        brand['nameBrand'] = brand['nameBrand'].replace('.', '_')
        brand['nameBrand'] = brand['nameBrand'].replace('(', '_')
        brand['nameBrand'] = brand['nameBrand'].replace(')', '_')
        brand['nameBrand'] = brand['nameBrand'].replace('+', '')
        model = row['model']
        model['name'] = re.sub(r'-|/|&|{|}|:', '_',  model['name'])
        model['name'] = model['name'].replace('.','_')
        model['name'] = model['name'].replace('(','_')
        model['name'] = model['name'].replace(')','_')
        model['name'] = re.sub(r'!|,|\s+', '', model['name'])
        model['name'] = model['name'].replace('+','')
        classe = row['model']['class']
        if classe:
            classes.append({
                'class': classe
            })
        brands.append(brand)
        model['nameBrand'] = brand['nameBrand']
        versions.append(model)
        models.append(model)
        fuels_aux = model['fuels']
        for fuel_aux in fuels_aux:
            if fuel_aux:
                obj_aux = {
                    'fuel': re.sub(r'\s+', '_', fuel_aux)
                }
                fuels.append(obj_aux)


    #Unique classes
    unique_classes = { each['class'] : each for each in classes }.values()

    #Unique fuels
    unique_fuels = { each['fuel'] : each for each in fuels }.values()

    # Unique brands array
    unique_brands = { each['nameBrand'] : each for each in brands }.values()

    # Unique models array
    unique_models = { each['name'] : each for each in models }.values()

    print('Num Fuels:', len(unique_fuels))
    print('Num Classes:', len(unique_classes))
    print('Num Brands:', len(unique_brands))
    print('Num Models:', len(unique_models))
    print('Num Versions:', len(versions))

    # Write fuels on ttl
    populate_fuels(unique_fuels)

    # Write unique classes on ttl
    populate_classes(unique_classes)

    # Write unique brands on ttl
    populate_brands(unique_brands)

    # Write unique models on ttl
    populate_model(unique_models)

    # Write all version on ttl
    populate_version(versions)
