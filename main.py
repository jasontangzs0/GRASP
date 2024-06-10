from environment import GridEnvironment
from agent import Agent


def check_energy_result(grid_string, agent_start_position, action_list, action_set, carry_limit, cost_per_Step):
    env = GridEnvironment(start=False)
    agent = Agent(agent_start_position[0], agent_start_position[1])
    env.load_grid(grid_string)

    if len(action_list) > 20:
        action_list = action_list[:20]

    for action in action_list:
        action = action.upper()
        if action_set == 1:
            action_list = ['UP', 'DOWN', 'LEFT', 'RIGHT', 'UPLEFT', 'UPRIGHT', 'DOWNLEFT', 'DOWNRIGHT']
        else:
            action_list = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        if action in action_list:
            env.move_agent(agent, action.lower())
        elif action == 'TAKE':
            if agent.energy < carry_limit:
                env.take_energy(agent)
        elif action == 'DROP':
            env.drop_all_energy(agent)

    return env.grid[agent.position[0]][agent.position[1]].energy  - cost_per_Step * len(action_list)



if __name__ == '__main__':
    check_energy_result('', [0, 0], [''], 0, 0, 0)
