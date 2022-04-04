#author: Meiru 

from prettytable import PrettyTable


def dijkstra(nodes, costs, start_node):
    """
    Dijkstra's algorithm for computing the maximum multiplicative cost from a start node to all other nodes.
    :param nodes: all unique nodes
    :param costs: costs from one node to another
    :param start_node: start node
    :return: maximum multiplicative cost from start node to all other nodes
    """
    unvisited_nodes = {node: None for node in nodes}
    visited_nodes = {}
    current_node = start_node
    current_cost = 1  # multiplicative so start with initial cost = 1
    unvisited_nodes[current_node] = current_cost
    while True:
        for neighbor, cost in costs[current_node].items():
            if neighbor not in unvisited_nodes:
                continue
            new_cost = current_cost * cost  # multiplicative cost
            if unvisited_nodes[neighbor] is None or new_cost > unvisited_nodes[neighbor]:
                unvisited_nodes[neighbor] = new_cost
        visited_nodes[current_node] = current_cost
        del unvisited_nodes[current_node]
        if not unvisited_nodes:
            break
        candidates = [node for node in unvisited_nodes.items() if node[1]]

        # we need the maximum, so sort from largest to smallest
        current_node, current_cost = sorted(candidates, key=lambda x: x[1], reverse=True)[0]
    return visited_nodes


def compute_exchange_rates(base_currency, currency_nodes, base_currency_exchange_rates, bid_fee=0.0, ask_fee=0.0):
    base_rates_per_currency = dict(zip(currency_nodes, base_currency_exchange_rates))

    # iterate over each currency
    #
    exchange_rates = {}
    for currency_node in currency_nodes:
        nodes = list(currency_nodes)
        start_node = currency_node

        costs = {base_currency: {}}
        for other_currency_node in currency_nodes:
            if other_currency_node == currency_node:
                costs[currency_node] = {}
                costs[currency_node][base_currency] = \
                    base_rates_per_currency[currency_node] * (1.0 - bid_fee / 100.0)
            else:
                costs[base_currency][other_currency_node] = \
                    1.0 / (base_rates_per_currency[other_currency_node] * (1.0 + ask_fee / 100.0))
                costs[other_currency_node] = {}
                costs[other_currency_node][base_currency] = \
                    1.0 / (base_rates_per_currency[other_currency_node] * (1.0 + ask_fee / 100.0))

        # compute least cost exchange rate via Dijkstra's algorithm
        exchange_rate_per_currency = dijkstra(nodes, costs, start_node)

        # store in exchange rates
        for currency in exchange_rate_per_currency.keys():
            exchange_rates[currency_node + currency] = exchange_rate_per_currency[currency]

    return exchange_rates


def print_exchange_rates(currency_nodes, exchange_rates):
    table = PrettyTable()
    headings = ['']
    headings.extend(currency_nodes)
    table.field_names = headings

    for currency_node in currency_nodes:
        row = [currency_node]
        for other_currency_node in currency_nodes:
            exchange_rate = exchange_rates[currency_node + other_currency_node]
            row.append("{:.8f}".format(exchange_rate))
        table.add_row(row)
    print(table)


def main():

    # original input with base currency = USD
    base_currency = 'USD'
    currency_nodes = ('USD', 'EUR', 'GBP', 'CAD', 'CNY', 'JPY')
    base_currency_exchange_rates = [1.0, 1.2363, 1.3762, 0.812018, 0.1558288, 0.0093493]
    bid_fee, ask_fee = 0.0, 0.0
    exchange_rates = compute_exchange_rates(base_currency, currency_nodes,
                                            base_currency_exchange_rates, bid_fee, ask_fee)
    print_exchange_rates(currency_nodes, exchange_rates)
    

    # change to base currency = CNY with appropriate exchange rates
    # first, concatenate the elements
    # second, change the exchange rates based on the updated index
    # third, change the index for looping
    base_currency = 'CNY'
    currency_nodes=('CNY','USD','EUR', 'GBP', 'CAD','JPY')
    index = 0
    for node in currency_nodes:
        exchange_rate = exchange_rates[node + base_currency]  
        base_currency_exchange_rates[index] = exchange_rate
        index += 1
    exchange_rates1 = compute_exchange_rates(base_currency, currency_nodes,
                                            base_currency_exchange_rates, bid_fee, ask_fee)
    print_exchange_rates(currency_nodes, exchange_rates1)
    
#print two tables to check
if __name__ == '__main__':
    main()
    
