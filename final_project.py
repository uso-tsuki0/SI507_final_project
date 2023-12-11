import interface

def main():
    print('Billboard Influence Network!')
    print('CAUTION: api querys may take more than 6 hours if cache is not used')
    cache = input('Do you want to use cache? (y/n): ')
    save = input('Do you want to save cache? (y/n): ')
    resume = input('Do you want to continue from last record? (y/n): ')
    cache = False if cache == 'n' else True
    save = False if save == 'n' else True
    resume = False if resume == 'n' else True
    headers = None
    if not cache:
        header_input = input('Please input the private key for wikipedia api if exists (y/n): ')
        if header_input == 'y':
            key = input('Please input the private key: ')
            user_agent = input('Please input the user agent: ')
            headers = {
                        'Authorization':f'Bearer {key}',
                        'User-Agent': user_agent
                    }
    itfc = interface.Interface()
    print('Loading...')
    try:
        itfc.get_content(cache=cache, save=save, resume=resume, header=headers)
    except:
        print('Error! Please check your internet connection and try again!')
        return False
    print('Done!')
    while True:
        print('Options:')
        print('1. Get billboard chart')
        print('2. Get artist information')
        print('3. Get shortest path between two artists')
        print('4. Get graph')
        print('5. Get rank by score')
        print('6. Get rank by number of songs')
        print('7. Get rank by influence activity')
        print('8. Exit')
        option = input('Please enter your option (1-8): ')
        if option == '8':
            print('Bye!')
            return False
        elif option == '1':
            itfc.query_billboard()
        elif option == '2':
            artist_name = input('Please enter artist name: ')
            itfc.query_artist(artist_name)
        elif option == '3':
            start = input('Please enter start artist name: ')
            end = input('Please enter end artist name: ')
            itfc.query_shortest_path(start, end)
        elif option == '4':
            itfc.query_graph()
        elif option == '5':
            itfc.query_rank_score()
        elif option == '6':
            itfc.query_rank_num()
        elif option == '7':
            itfc.query_rank_active()
        else:
            print('Invalid option!')
        resume = input('Do you want to continue? (y/n) :')
        if resume == 'n':
            print('Bye!')
            return False

if __name__ == '__main__':
    main()