from optimize import Optimize

if __name__ == '__main__':
    solution, fitness = Optimize.naive_approach()
    Optimize.draw_solution(solution)