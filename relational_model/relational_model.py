from unicodedata import name
from IPython.display import display, Markdown
import math

WILDCARD = "*"

def compareLists(should, given):

    badCount = 0
    should_cpy = should.copy()
    given_copy = given.copy()
    given_copy = [w.split("_")[-1] for w in given_copy]
    should_cpy = [w.split("_")[-1] for w in should_cpy]

    for a in given_copy:
        if a not in should_cpy:
            if WILDCARD in should_cpy:
                should_cpy.remove(WILDCARD)
            else:
                badCount += 1  # Superfluous item in given

    # In a correct solution, all wildcards should be removed by now

    for a in should_cpy:
        if a not in given_copy:
            badCount += 1  # Missing item in given

    return badCount


class RM:
    relations = []
    subsets = []
    intersections = []

    def __init__(self):
        self.relations = []
        self.subsets = []
        self.intersections = []
        return

    def addRelation(self, relation):
        for r in self.relations:
            if relation.name == r.name:
                print(f"Fehler: Relation mit Name {r.name} wurde bereits hinzugefügt.")
                return
        self.relations.append(relation)

    def addDependency(self, dependency):
        if str(dependency.__class__.__name__) == "Subset":
            self.subsets.append(dependency)
            return
        if str(dependency.__class__.__name__) == "Intersection":
            self.intersections.append(dependency)
            return
        print("Fehler: An addDependency sollte entweder ein Subset oder eine Intersection übergeben werden.")
        print("Es wurde ein " + dependency.__class__.__name__ + " übergeben.")

    def getNumRelations(self):
        return len(self.relations)

    def getNumDependencies(self):
        return len(self.subsets) + len(self.intersections)

    def display(self):
        for r in self.relations:
            r.display()
        for s in self.subsets:
            s.display()
        for i in self.intersections:
            i.display()

        if (len(self.relations) + len(self.subsets) + len(self.intersections) == 0):
            display(Markdown("(empty Relation)"))


    def get_scaled_score(self, rm, scores, max_points, debug=False):
        worst_score = self.compare_against(RM(), scores, False)
        score = self.compare_against(rm, scores, debug)
        penalty = round((score / worst_score) * max_points)
        result = max(0, max_points - penalty)
        print(f"Scale deducted points to exercise's total points: {penalty}")
        print(f"Result: {result} / {max_points} points achieved")
        return result

    def compare_against(self, rm, scores, debug=False):
        score = 0

        if (debug):
            print("Checking relations...")

        # 1. Check relations
        for r1 in self.relations:
            for r2 in rm.relations:
                if r1.name == r2.name:
                    print(f"Found relation {r1.name}")
                    missingPrimaries = compareLists(
                        r1.primaryKeys, r2.primaryKeys)
                    missingNormal = compareLists(
                        r1.attributeList, r2.attributeList)

                    penalty = scores["wrong_attribute"] * \
                        (missingPrimaries + missingNormal)
                    score += penalty

                    if debug:
                        #if missingPrimaries > 0:
                        #    print(f"Wrong primary keys: {missingPrimaries}")
                        #if missingNormal > 0:
                        #    print(f"Wrong normal attributes: {missingNormal}")
                        if (penalty > 0):
                            print(f"Wrong attributes in relation '{r1.name}': deducting {penalty} points")

                    break
            else:
                missingRelationPenalty =  scores["wrong_relation"] + scores["wrong_attribute"] * \
                    (len(r1.primaryKeys) + len(r1.attributeList))
                score += missingRelationPenalty
                if debug:
                    print(f"Missing relation '{r1.name}': deducting {missingRelationPenalty} points")

        if debug:
            print("Checking subsets...")

        # 2. Check subsets
        for s1 in self.subsets:

            curr_best = None
            curr_best_score = 10000

            for s2 in rm.subsets:
                if s1.lhs.relationName == s2.lhs.relationName and s1.rhs.relationName == s2.rhs.relationName:
                    # Found correct subset
                    # Check attributes
                    missingLhs = compareLists(
                        s1.lhs.attributes, s2.lhs.attributes)
                    missingRhs = compareLists(
                        s1.rhs.attributes, s2.rhs.attributes)
                    curr_score = scores["wrong_attribute"] * \
                        (missingLhs + missingRhs)
                    if (curr_score < curr_best_score):
                        if curr_best is not None:
                            print("New best")
                        curr_best_score = curr_score
                        curr_best = s2

            if curr_best is None:
                penalty = scores["wrong_subset"] + scores["wrong_attribute"] * \
                    (len(s1.rhs.attributes) + len(s1.lhs.attributes))
                score += penalty
                if debug:
                    print(
                        f"Missing subset lhs={s1.lhs.relationName}, rhs={s1.rhs.relationName}: deducting {penalty} points")
            else:
                if debug:
                    #if missingLhs > 0:
                    #    print(f"Wrong attributes on left side: {missingLhs}")
                    #if missingRhs > 0:
                    #    print(f"Wrong attributes on right side: {missingRhs}")
                    if (curr_best_score > 0):
                        print(f"Wrong attributes in subset lhs={s1.lhs.relationName}, rhs={s1.rhs.relationName}: deducting {curr_best_score} points")
                score += curr_best_score

        if debug:
            print("Checking intersections...")

        # 3. Check intersections

        # DIRTY HACK BECAUSE OF AMBIGUITY OF SOLUTION
        # JUST COUNT NUMBER OF INTERSECTIONS
        missingIntersectionPenalty = max(0, len(self.intersections) -
                     len(rm.intersections)) * scores["wrong_intersection"]
        score += missingIntersectionPenalty
        if (missingIntersectionPenalty > 0):
            if debug:
                print(f"Missing intersections: deducting {missingIntersectionPenalty} points")


#        for i1 in self.intersections:
#            for i2 in rm.intersections:
#                if s1.lhs.relationName == s2.lhs.relationName and s1.rhs.relationName == s2.rhs.relationName:
#                    # Found correct intersection
#                    # Check attributes
#                    missingLhs = compareLists(i1.lhs.attributes, i2.lhs.attributes)
#                    missingRhs = compareLists(i1.rhs.attributes, i2.rhs.attributes)
#                    if debug:
#                        if missingLhs > 0:
#                            print(f"Wrong attributes on left side: {missingLhs}")
#                        if missingRhs > 0:
#                            print(f"Wrong attributes on right side: {missingRhs}")
#                    score += scores["wrong_attribute"] * (missingLhs + missingRhs)
#                    break
#            else:
#                if debug:
#                    print(f"Missing intersection lhs={i1.lhs.relationName}, rhs={i1.rhs.relationName}")
#                score += scores["wrong_intersection"]
#                score += scores["wrong_attribute"] * (len(i1.rhs.attributes) + len(i1.lhs.attributes))

        if debug:
            print(f"Total deducted points: {score}")

        return score


class ProjectedRelation:
    relationName = ""
    attributes = []

    def __init__(self, relationName, attributes):
        self.relationName = relationName
        self.attributes = attributes

    def getMarkdown(self):
        return self.relationName \
            + "[" \
            + ", ".join(self.attributes) \
            + "]"

    def display(self):
        display(Markdown(self.getMarkdown()))

    def compareTo(self, projectedRelation):
        if (self.relationName != projectedRelation.relationName):
            return 0
        return max(0, compareLists(self.attributes, projectedRelation.attributes))


class Relation:
    name = ""
    attributeList = []  # Excluding primary keys???
    primaryKeys = []

    def __init__(self, name, primaryKeys, attributeList):
        self.name = name
        self.attributeList = attributeList
        self.primaryKeys = primaryKeys

    def getMarkdown(self):
        return self.name \
            + "(" \
            + ", ".join(map(lambda x: "<u>" + x + "</u>", self.primaryKeys)) \
            + ("" if len(self.primaryKeys) == 0 or len(self.attributeList) == 0 else ", ") \
            + ", ".join(self.attributeList) \
            + ")"

    def display(self):
        display(Markdown(self.getMarkdown()))

    def compareTo(self, relation):
        if (self.name != relation.name):
            return 0
        return max(0, compareLists(self.attributeList, relation.attributeList)
                   + compareLists(self.primaryKeys, relation.primaryKeys))


class Subset:
    lhs = None  # Takes a projected relation
    rhs = None  # Takes a projected relation

    def __init__(self, lhs, rhs):
        # if ((not isinstance(lhs, ProjectedRelation)) or (not isinstance(rhs, ProjectedRelation))):
        #print("Fehler: An ein Subset sollten zwei ProjectedRelations übergeben werden")
        self.lhs = lhs
        self.rhs = rhs

    def getMarkdown(self):
        return self.lhs.getMarkdown() + " ⊆ " + self.rhs.getMarkdown()

    def display(self):
        display(Markdown(self.getMarkdown()))

    def compareTo(self, subset):
        return self.lhs.compareTo(subset.lhs) + self.rhs.compareTo(subset.rhs)


class Intersection:
    lhs = None
    rhs = None
    equals = ""

    def __init__(self, lhs, rhs, equals):
        # if ((not isinstance(lhs, ProjectedRelation)) or (not isinstance(rhs, ProjectedRelation))):
        #print("Fehler: An eine Intersection sollten zwei ProjectedRelations übergeben werden")
        self.lhs = lhs
        self.rhs = rhs
        self.equals = equals

    def getMarkdown(self):
        return self.lhs.getMarkdown() + " ∩ " + self.rhs.getMarkdown() + " = " + self.equals

    def display(self):
        display(Markdown(self.getMarkdown()))

    def compareTo(self, intersection):
        # self.equals will not be tested
        return self.rhs.compareTo(intersection.rhs) + self.lhs.compareTo(intersection.lhs)
