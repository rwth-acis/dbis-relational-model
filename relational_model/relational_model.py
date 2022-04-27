def compareLists(given, should):
    correctCount = 0
    for a in given:
        if a in should:
            correctCount += 1
        else:
            correctCount -= 1

class ProjectedRelation:
    relationName = ""
    attributes = []

    def __init__(self, relationName, attributes):
        self.relationName = relationName
        self.attributes = attributes

    def print(self):
        print(f'{self.relation.name}[{", ".join(self.attributes)}"]')

    def compareTo(self, projectedRelation):
        if (self.name != projectedRelation.name): return 0
        return max(0, compareLists(self.attributes, projectedRelation.attributes))


class Relation:
    name = ""
    attributeList = [] # Excluding primary keys???
    primaryKeys = []

    def __init__(self, name, attributeList, primaryKeys):
        self.name = name
        self.attributeList = attributeList
        self.primaryKeys = primaryKeys

    def print(self):
        print(f'{self.relation}(<u>{", ".join(self.primaryKeys)}</u>, {", ".join(self.attributes)}")')

    def compareTo(self, relation):
        if (self.name != relation.name): return 0
        return max(0, compareLists(self.attributeList, relation.attributeList)
            + compareLists(self.primaryKeys, relation.primaryKeys))


class Subset:
    lhs
    rhs

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def print(self):
        lhs.print()
        print("⊆")
        rhs.print()

    def compareTo(self, subset):
        return self.lhs.compareTo(subset.lhs) + self.rhs.compareTo(subset.rhs)

class Intersection:
    lhs
    rhs
    equals

    def __init__(self, lhs, rhs, equals):
        self.lhs = lhs
        self.rhs = rhs
        self.equals = equals

    def print(self):
        self.lhs.print()
        print("∩")
        self.rhs.print()
        print("=")
        if (self.equals == "emptyset"):
            print("∅")
        else:
            print(self.equals)

    def compareTo(self, intersection):
        if (self.equals != intersection.equals): return 0
        return self.rhs.compareTo(intersection.rhs) + self.lhs.compareTo(intersection.lhs)


class ERTransformationResult:
    erTree = None
    relations = None
    interrelationalDependenciesSubsets = None
    weakEntitiesIntersections = None
    isASubsets = None
    bigAttributesSubsets = None
    recursionSubsets = None
    ternaryRelationSubsets = None

    def __init__(self, erTree, relations,
        interrelationalDependenciesSubsets,
        weakEntitiesIntersections,
        isASubsets,
        bigAttributesSubsets,
        recursionSubsets,
        ternaryRelationSubsets):
        self.erTree = erTree
        self.relations = relations
        self.interrelationalDependenciesSubsets = interrelationalDependenciesSubsets
        self.weakEntitiesIntersections = weakEntitiesIntersections
        self.isASubsets = isASubsets
        self.bigAttributesSubsets = bigAttributesSubsets
        self.recursionSubsets = recursionSubsets
        self.ternaryRelationSubsets = ternaryRelationSubsets
