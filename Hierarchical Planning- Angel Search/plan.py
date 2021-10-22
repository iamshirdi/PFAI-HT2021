from aima.planning import HLA,AngelicHLA,AngelicNode,RealWorldPlanningProblem
import aima
# Get to airport problem
def get_to_airport1():
    # Hierarchy of possible actions, one level of High Level Actions and 
    # one level of primitive actions 
    library = {'HLA': [
        'Go(Home,SFO)', 
        'Go(Home,SFO)', 
        'Drive(Home, SFOLongTermParking)',
        'Shuttle(SFOLongTermParking, SFO)', 
        'Taxi(Home, SFO)'
        ],
        'steps': [
        ['Drive(Home, SFOLongTermParking)', 'Shuttle(SFOLongTermParking, SFO)'],
        ['Taxi(Home, SFO)'],
        [], [], []
        ],
        'precond': [
        ['At(Home) & Have(Car)'],
        ['At(Home)'],
        ['At(Home) & Have(Car)'],
        ['At(SFOLongTermParking)'],
        ['At(Home) & Have(Cash)']
        ],
        'effect': [
        ['At(SFO) & ~At(Home)'], 
        ['At(SFO) & ~At(Home) & ~Have(Cash)'],
        ['At(SFOLongTermParking) & ~At(Home)'], 
        ['At(SFO) & ~At(LongTermParking)'], 
        ['At(SFO) & ~At(Home) & ~Have(Cash)']
        ]}
   
    # Possible HLA actions
    go_SFO = HLA('Go(Home,SFO)', precond='At(Home)', effect='At(SFO) & ~At(Home)')
    drive_SFOLongTermParking = HLA('Drive(Home, SFOLongTermParking)', 'At(Home) & Have(Car)','At(SFOLongTermParking) & ~At(Home)')
    taxi_SFO = HLA('Taxi(Home,SFO)', precond='At(Home) & Have(Cash)', effect='At(SFO) & ~At(Home) & ~Have(Cash)')   
    shuttle_SFO = HLA('Shuttle(SFOLongTermParking, SFO)', 'At(SFOLongTermParking)', 'At(SFO) & ~At(LongTermParking)')
    
    # Define the problem 
    problem = RealWorldPlanningProblem('At(Home) & Have(Cash) & Have(Car)', 'At(SFO) & Have(Cash)', [taxi_SFO, go_SFO, drive_SFOLongTermParking, shuttle_SFO])
    angelic_opt_description = AngelicHLA('Go(Home, SFO)', precond = 'At(Home)', effect ='$+At(SFO) & $-At(Home)' ) 
    angelic_pes_description = AngelicHLA('Go(Home, SFO)', precond = 'At(Home)', effect ='$+At(SFO) & ~At(Home)' ) #may or may not be at home ~

    initialPlan = [AngelicNode(problem.initial, None, [angelic_opt_description], [angelic_pes_description])]
    
    opt_reachable_set = RealWorldPlanningProblem.reach_opt(problem.initial, initialPlan[0])
    pes_reachable_set = RealWorldPlanningProblem.reach_pes(problem.initial, initialPlan[0])
    print('Possible reachable set of states in a optimistic scenario')
    print([x for y in opt_reachable_set.keys() for x in opt_reachable_set[y]], '\n')
    print('Possible reachable set of states in a pessimistic scenario')
    print([x for y in pes_reachable_set.keys() for x in pes_reachable_set[y]])
    
    print('Print our refinements') 
    for sequence in RealWorldPlanningProblem.refinements(go_SFO, library):
        print (sequence)
        print([x.__dict__ for x in sequence ], '\n')
    
    print('Do planning')
    plan = problem.angelic_search(library, initialPlan)
    
    print('Final plan')
    print ([x.__dict__ for x in plan])


def get_to_airport2():
    # Hierarchy of possible actions, one level of High Level Actions and 
    # one level of primitive actions 
    library = {'HLA': [
        'Go(Home,SFO)', 
        'Go(Home,SFO)', 
        'Drive(Home, SFOLongTermParking)',
        'Shuttle(SFOLongTermParking, SFO)', 
        'Taxi(Home, SFO)'
        ],
        'steps': [
        ['Drive(Home, SFOLongTermParking)', 'Shuttle(SFOLongTermParking, SFO)'],
        ['Taxi(Home, SFO)'],
        [], [], []
        ],
        'precond': [
        ['At(Home) & Have(Car)'],
        ['At(Home)'],
        ['At(Home) & Have(Car)'],
        ['At(SFOLongTermParking)'],
        ['At(Home)']
        ],
        'effect': [
        ['At(SFO) & ~At(Home)'], 
        ['At(SFO) & ~At(Home) '],
        ['At(SFOLongTermParking) & ~At(Home)'], 
        ['At(SFO) & ~At(LongTermParking)'], 
        ['At(SFO) & ~At(Home) ']
        ]}
   
    # Possible HLA actions
    go_SFO = HLA('Go(Home,SFO)', precond='At(Home)', effect='At(SFO) & ~At(Home)')
    go_SFO_car = HLA('Go(Home,SFO)', precond='At(Home) & Have(Car)', effect='At(SFO) & ~At(Home)')
    drive_SFOLongTermParking = HLA('Drive(Home, SFOLongTermParking)', 'At(Home) & Have(Car)','At(SFOLongTermParking) & ~At(Home)')
    taxi_SFO = HLA('Taxi(Home,SFO)', precond='At(Home) & Have(Cash)', effect='At(SFO) & ~At(Home)')   
    shuttle_SFO = HLA('Shuttle(SFOLongTermParking, SFO)', 'At(SFOLongTermParking)', 'At(SFO) & ~At(LongTermParking)')
    
    # Define the problem 
    problem = RealWorldPlanningProblem('At(Home)', 'At(SFO)', [go_SFO_car, go_SFO, taxi_SFO, drive_SFOLongTermParking, shuttle_SFO])
    angelic_opt_description = AngelicHLA('Go(Home, SFO)', precond = 'At(Home)', effect ='$+At(SFO) & $-At(Home)' ) 
    angelic_pes_description = AngelicHLA('Go(Home, SFO)', precond = 'At(Home)', effect ='$+At(SFO) & ~At(Home)' ) #may or may not be at home ~

    initialPlan = [AngelicNode(problem.initial, None, [angelic_opt_description], [angelic_pes_description])]
    
    opt_reachable_set = RealWorldPlanningProblem.reach_opt(problem.initial, initialPlan[0])
    pes_reachable_set = RealWorldPlanningProblem.reach_pes(problem.initial, initialPlan[0])
    print('Possible reachable set of states in a optimistic scenario')
    print([x for y in opt_reachable_set.keys() for x in opt_reachable_set[y]], '\n')
    print('Possible reachable set of states in a pessimistic scenario')
    print([x for y in pes_reachable_set.keys() for x in pes_reachable_set[y]])
    
    print('Print our refinements') 
    for sequence in RealWorldPlanningProblem.refinements(go_SFO, library):
        print (sequence)
        print([x.__dict__ for x in sequence ], '\n')
    
    print('Do planning')
    plan = problem.angelic_search(library, initialPlan)
    
    print('Final plan')
    print ([x.__dict__ for x in plan])

# Example 2
def get_airport_3():
    library_2 = {
            'HLA': [
                'Go(Home,SFO)', 
                'Go(Home,SFO)', 
                'Bus(Home, MetroStop)',
                'Metro(MetroStop, SFO)', 
                'Metro(MetroStop, SFO)',
                'Metro1(MetroStop, SFO)',
                'Metro2(MetroStop, SFO)',
                'Taxi(Home, SFO)'],
            'steps': [
                ['Bus(Home, MetroStop)', 'Metro(MetroStop, SFO)'], 
                ['Taxi(Home, SFO)'],
                [],
                ['Metro1(MetroStop, SFO)'], 
                ['Metro2(MetroStop, SFO)'],
                [],
                [],
                []],
            'precond': [
                ['At(Home)'],
                ['At(Home)'],
                ['At(Home)'],
                ['At(MetroStop)'],
                ['At(MetroStop)'],
                ['At(MetroStop)'], 
                ['At(MetroStop)'] ,
                ['At(Home) & Have(Cash)']],
            'effect': [
                ['At(SFO) & ~At(Home)'],
                ['At(SFO) & ~At(Home) & ~Have(Cash)'],
                ['At(MetroStop) & ~At(Home)'],
                ['At(SFO) & ~At(MetroStop)'],
                ['At(SFO) & ~At(MetroStop)'], 
                ['At(SFO) & ~At(MetroStop)'] , 
                ['At(SFO) & ~At(MetroStop)'] ,
                ['At(SFO) & ~At(Home) & ~Have(Cash)']] 
            }



    # Possible HLA actions
    go_SFO = HLA('Go(Home,SFO)', precond='At(Home)', effect='At(SFO) & ~At(Home)')
    go_SFO_bus = HLA('Go(Home,SFO)', precond='At(Home)', effect='At(MetroStop) & ~At(Home)')
    taxi_SFO = HLA('Taxi(Home,SFO)', precond='At(Home) & Have(Cash)', effect='At(SFO) & ~At(Home)')   
    metro_SFO =HLA('Metro(MetroStop, SFO)', precond='At(MetroStop)', effect='At(SFO) & ~At(MetroStop)')
    metro1_SFO =HLA('Metro1(MetroStop, SFO)', precond='At(MetroStop)', effect='At(SFO) & ~At(MetroStop)')
    metro2_SFO =HLA('Metro2(MetroStop, SFO)', precond='At(MetroStop)', effect='At(SFO) & ~At(MetroStop)')

    # Define the problem 
    problem = RealWorldPlanningProblem('At(Home) & Have(Cash)', 'At(SFO)  & Have(Cash)', [go_SFO_bus, go_SFO, metro_SFO, metro1_SFO, metro2_SFO,taxi_SFO])
    angelic_opt_description = AngelicHLA('Go(Home, SFO)', precond = 'At(Home)', effect ='$+At(SFO) & $-At(Home)' ) 
    angelic_pes_description = AngelicHLA('Go(Home, SFO)', precond = 'At(Home)', effect ='$+At(SFO) & ~At(Home)' ) #may or may not be at home ~

    initialPlan = [AngelicNode(problem.initial, None, [angelic_opt_description], [angelic_pes_description])]
    
    opt_reachable_set = RealWorldPlanningProblem.reach_opt(problem.initial, initialPlan[0])
    pes_reachable_set = RealWorldPlanningProblem.reach_pes(problem.initial, initialPlan[0])
    print('Possible reachable set of states in a optimistic scenario')
    print([x for y in opt_reachable_set.keys() for x in opt_reachable_set[y]], '\n')
    print('Possible reachable set of states in a pessimistic scenario')
    print([x for y in pes_reachable_set.keys() for x in pes_reachable_set[y]])
    
    print('Print our refinements') 
    for sequence in RealWorldPlanningProblem.refinements(go_SFO, library_2):
        print (sequence)
        print([x.__dict__ for x in sequence ], '\n')
    
    print('Do planning')
    plan2 = problem.angelic_search(library_2, initialPlan)
    print("plan....................................... HLA ", plan2)
    print('Final plan')
    print ([x.__dict__ for x in plan2])




def main():
    # Get to airport problem
    get_to_airport2()
    get_airport_3()
    
if __name__ == "__main__": main()