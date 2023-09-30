from owlready2 import *
import random


class MyOntology:
    def __init__(self, onto_file, label_property):
        self.onto_file = onto_file
        self.onto = get_ontology(onto_file).load()
        self.label_property = label_property
        self.graph = default_world.as_rdflib_graph()
        self.iri_label = dict()
        for p in self.label_property:
            q = 'SELECT ?s ?o WHERE {?s <%s> ?o.}' % p
            for res in list(self.graph.query(q)):
                iri = res[0].n3()[1:-1]
                lit = res[1]
                if hasattr(lit, 'language') and (lit.language is None or lit.language == 'en' or
                                                 lit.language == 'en-us' or lit.language == 'en-gb'):
                    if iri in self.iri_label:
                        if lit.value not in self.iri_label[iri]:
                            self.iri_label[iri].append(lit.value)
                    else:
                        self.iri_label[iri] = [lit.value]
        self.named_classes = self.get_named_classes()
        self.className_label = dict()
        for c_iri in self.iri_label:
            self.className_label[str(IRIS[c_iri])] = self.iri_label[c_iri]

        self.name_restrictions = dict()
        self.restrictions = set()
        self.restrictionsName_label = dict()
        for c in self.named_classes:
            for parent in c.is_a:
                if self.is_target_some_restriction(c=parent):
                    self.name_restrictions[str(parent)] = parent
                    self.restrictions.add(parent)
                    if str(parent) not in self.restrictionsName_label:
                        self.restrictionsName_label[str(parent)] = self.restriction_to_label(restriction=parent)

    '''
        Generate descriptions towards a restriction
        involving properties of FoodOn:
        {'composed primarily of', 'derives from', 'develops from', 'has consumer', 'has country of origin',
            'has defining ingredient', 'has food substance analog', 'has ingredient', 'has input', 'has member',
            'has output', 'has part', 'has participant', 'has quality', 'has substance added', 'in taxon',
            'input of', 'is about', 'member of', 'output of', 'part of', 'produced by', 'surrounded by'}
    '''

    def restriction_to_label(self, restriction):
        p_label = restriction.property.label[0]
        if not (p_label.endswith('of') or p_label.endswith('from') or p_label.endswith('by')
                or p_label.endswith('about')):
            p_label = p_label + ' of'

        descriptions = list()
        if ' | ' in str(restriction.value):
            desc = 'something %s ' % p_label
            names = list()
            for item in str(restriction.value).split(' | '):
                names.append(self.className_label[item][0])
            desc = desc + ' ' + ' or '.join(names)
            descriptions.append(desc)

        elif ' & ' in str(restriction.value):

            # this is a special case with Not in FoodOn
            if str(restriction.value) == 'obo.FOODON_00002275 & obo.FOODON_00003202 & Not(obo.FOODON_00001138)':
                desc = 'something %s %s and %s and not %s' % (p_label, self.className_label['obo.FOODON_00002275'][0],
                                                              self.className_label['obo.FOODON_00003202'][0],
                                                              self.className_label['obo.FOODON_00001138'][0])
                descriptions.append(desc)

            else:
                desc = 'something %s ' % p_label
                names = list()
                for item in str(restriction.value).split(' & '):
                    names.append(self.className_label[item][0])
                desc = desc + ' ' + ' and '.join(names)
                descriptions.append(desc)

        else:
            for lab in self.className_label[str(restriction.value)]:
                desc = 'something %s %s' % (p_label, lab)
                descriptions.append(desc)
        return descriptions

    @staticmethod
    def is_target_some_restriction(c):
        if type(c) == class_construct.Restriction and c.type == 24 and type(c.property) == prop.ObjectPropertyClass \
                and type(c.value) == ThingClass and ('some' not in str(c.value) and 'only' not in str(c.value) and
                                                     'min' not in str(c.value) and 'exactly' not in str(
                    c.value) and 'max' not in str(c.value)):
            return True
        else:
            return False

    '''
        Get named classes that are not deprecated (excluding OWL Thing)
    '''

    def get_named_classes(self):
        named_classes = list()
        for c in self.onto.classes():
            if True not in c.deprecated and not c == owl.Thing:
                named_classes.append(c)
        return named_classes

    '''
        Given a named subclass, get a negative class for a negative subsumption
        The current implementation does not consider masked subsumptions
    '''

    def get_negative_sample(self, subclass_str, subsumption_type='named class'):
        subclass = IRIS[subclass_str]
        if subsumption_type == 'named class':
            neg_c = random.sample(set(self.named_classes) - subclass.ancestors(), 1)[0]
            return neg_c.iri
        else:
            restrictions_ancestors = self.get_all_restriction_ancestors(cls=subclass)
            neg_c = random.sample(self.restrictions - restrictions_ancestors, 1)[0]
            return str(neg_c)

    @staticmethod
    def get_all_restriction_ancestors(cls):
        ancs = set()
        for c in cls.is_a:
            if type(c) == class_construct.Restriction:
                ancs.add(c)
        for ancestor in cls.ancestors():
            for c in ancestor.is_a:
                if type(c) == class_construct.Restriction:
                    ancs.add(c)
        return ancs

    '''
        Get declared subsumptions whose parents are named classes (excluding OWL Thing)
    '''

    def get_declared_named_class_subsumption(self):
        declared_subsumptions = list()
        for c in self.named_classes:
            for parent in c.is_a:
                if self.is_normal_named_class(parent):
                    declared_subsumptions.append([c, parent])
        return declared_subsumptions


    @staticmethod
    def is_normal_named_class(c):
        if type(c) == entity.ThingClass and c is not owl.Thing and True not in c.deprecated:
            return True
        else:
            return False




