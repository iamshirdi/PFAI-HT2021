'''
Define problem and start execution of search problems

Author: Tony Lindgren
'''

from missionaries_and_cannibals import MissionariesAndCannibals 
from eight_puzzle import EightPuzzle
from node_and_search import SearchAlgorithm

init_state = [[0, 0], 'r', [3, 3]] 
goal_state = [[3, 3], 'l', [0, 0]] 

# i_state = [[3,1,2],['e',4,5],[6,7,8]]
i_state = [[7,2,4],[5,'e',6],[8,3,1]]
g_state = [['e',1,2],[3,4,5],[6,7,8]]

def main():

    ep = EightPuzzle(i_state,g_state)
    sa = SearchAlgorithm(ep)
    print('Greedy Algorithm')
    print('Start state: ')
    ep.pretty_print()
    solution = sa.greedy_search(statistics=True)
    print('goal state: ')
    solution.state.pretty_print()
    # solution path
    solution.pretty_print_solution(verbose=True)


    # mc = MissionariesAndCannibals(init_state, goal_state)
    # sa = SearchAlgorithm(mc)
    
    # print('BFS')
    # print('Start state: ')
    # mc.pretty_print()
    # solution = sa.bfs(statistics=True)
    # print('goal state: ')
    # solution.state.pretty_print()
    # # solution path
    # solution.pretty_print_solution(verbose=True)

    # print('DFS')
    # print('Start state: ')
    # mc.pretty_print()
    # solution = sa.dfs(statistics=True)
    # print('goal state: ')
    # solution.state.pretty_print()
    # solution.pretty_print_solution(verbose=True)

    # print('IDFS')
    # print('Start state: ')
    # mc.pretty_print()
    # solution = sa.idfs(statistics=True)
    # print('goal state: ')
    # solution.state.pretty_print()
    # solution.pretty_print_solution(verbose=True)


if __name__ == "__main__":
    main()