#DOMINOES
import random
import os

#generates set of tiles
class Tile:
    def __init__(self):
        self.tiles=[]
        for i in range(7):
            for j in range(i+1):
                self.tiles.append([j,i])
        #print('DoubleSix:\n',self.tiles)

class DoubleSix(Tile):
    def __init__(self,no):
        Tile.__init__(self)
        self.no_pl=no
        self.sett={}

    def create_play_tiles(self):
        self.play_tiles=random.sample(self.tiles,k=7* self.no_pl)
        #print('play_tiles:\n',self.play_tiles)

    def distribute(self):
        j=0
        for i in range(self.no_pl):
            self.sett[i+1]=self.play_tiles[j:j+7]
            j+=7
        #print('distributed:\n',self.set)
        return self.sett

class Player:
    def __init__(self,n):
        self.player_names={}
        print('\nENTER USERNAMES:')
        for i in range(1,n+1):
            print('\tPlayer ',i,' : ',end=' ')
            self.player_names[i]=input()


class LineOfPlay(Player):
    def __init__(self, n,comp):
        Player.__init__(self,n)

        if comp==1 :
            self.no_players=2
            self.player_names[2]='Computer'
            print('\tPlayer ',2,' : ',self.player_names[2])
        else:
            self.no_players = n
        self.total_points={}
        for i in range(1,self.no_players+1):
            self.total_points[i]=0


    def reset(self):
        self.playlist=[]
        self.set={}
        self.points={}
        self.cur_points={}

        for i in range(1,self.no_players+1):
            self.points[i]=0
            self.cur_points[i]=0

        dsix=DoubleSix(self.no_players)
        dsix.create_play_tiles()
        self.set = dsix.distribute()
        #print(self.set)

    def display_tiles(self,pno):
        print('Your Tiles:\n',self.set[pno])

    def ends(self):
        if self.playlist != []:
            front=self.playlist[0][0]
            back=self.playlist[len(self.playlist)-1][1]
            self.end_nos=[front,back]
            #print('ends: ',self.end_nos)
        else:
            self.end_nos=[]

    def playing(self,pno,index,comp):
        #index=int(input('choose(index no): '))
        #self.ends()
        if index>=len(self.set[pno]):
            print('INVALID INDEX!!')
            print('please choose again..')
            return -1

        chosen=self.set[pno][index]
        print('Chosen tile: ',chosen)

        op={'00':0,'01':1,'10':2,'11':3}
        flag=[]
        flag_pos={0:0,1:len(self.playlist),2:0,3:len(self.playlist)}  #flag with pos
        finish=-1

        #finding pos to insert if correct tile
        if self.playlist != []:

            for i in range(2):
                for j in range(2):
                    if chosen[i]==self.end_nos[j]:
                        key=str(i)+str(j)
                        flag.append(op[key])

            #print(flag)
            if len(flag)>1:
                if flag_pos.get(flag[0])==flag_pos.get(flag[1]):
                    flag.remove(flag[1])
                else:
                    while finish==-1:
                        if comp==1 and pno==2:
                            ch='f'
                        else:
                            print('You have to choose where to play your tile')
                            print('f:front\nb:back')
                            ch=input('Enter choice: ')

                        if ch=='f':
                            pos=0
                        elif ch=='b':
                            pos=len(self.playlist)
                        else:
                            print('invalid choice!')
                            continue

                        #print(pos)
                        f=[]
                        for key in flag_pos.keys():
                            if flag_pos[key]==pos and key in flag:
                                f=[key]
                        flag=f
                        finish=1


            if flag==[]:
                final_pos=-1
            else:
                #print('STATUS...')
                #print(flag)
                final_pos=flag_pos.get(flag[0])
                #print('final position: ',final_pos)
                if flag==[0] or flag==[3]:
                    chosen.reverse()

        else:
            final_pos=0

        #inserting otherwise prompting user to choose again
        if final_pos !=-1:
            self.set[pno].remove(chosen)
            self.playlist.insert(final_pos,chosen)
            return 1
        else:
            print('You cannot play that tile!')
            print('You can only play these...')
            return -1

    def choose_tile(self,pno,comp):
        self.ends()
        choose_tiles=[]
        if self.end_nos != []:
            for tile in self.set[pno]:
                y=0
                for no in tile:
                    if no in self.end_nos:
                        y=1
                if y == 1:
                    choose_tiles.append(tile)
                else:
                    choose_tiles.append('XXXX')

            if comp==0 or (comp==1and pno==1):
                print(choose_tiles)

            for i in choose_tiles:
                if i != 'XXXX':
                    return 1,choose_tiles.index(i)    #means not blocked and returning 1st tile index
            return -1 ,10  #means block

        else:
            print('All your tiles:')
            print(self.set[pno])
            return 1,10    #10 for no tile chosen(for comp)

    #def comp_play(self,pno):


    def check_block(self,block_res):
        res= block_res[len(block_res)-self.no_players:]
        if res == [-1]*self.no_players:
            return 1    #means game's blocked
        else:
            return -1

    def tiles_empty(self,pno):
        if len(self.set[pno])==0:
            return 1
        else:
            return -1

    def current_round_winner(self,pno,type_gameover):
        #calculating points
        winner=-1

        #finding winner for current round......start here
        if type_gameover==1:
            winner=pno
        if type_gameover == 2:
            winners=[]
            for s in self.set.keys():
                for i in self.set[s]:
                    for n in i:
                        self.points[s]+=n

            for key in self.points.keys():
                if self.points[key]==min(self.points.values()):
                    winners.append(key)

            if len(winners)==1:
                winner=winners[0]
            else:   #if min points are shared by more than 1 player..lightest tile ..winner
                light_tile=[]
                for p in winners:
                    tile_sum=[]
                    for t in self.set[p]:
                        sum=0
                        for no in t:
                            sum+=no
                            tile_sum.append(sum)

                    light_tile.append(min(tile_sum))

                #print(min(light_tile))
                wind=light_tile.index(min(light_tile))
                winner=winners[wind]

        return winner

    def calc_points_winner(self,pno,type):
        win=self.current_round_winner(pno,type)
        sum=0
        for s in self.set.keys():
            if s != win:
                for i in self.set[s]:
                    for n in i:
                        sum+=n
        self.cur_points[win]=sum
        self.total_points[win]+=sum


        #finding winner
        winner_points=max(self.total_points.values())
        winner=[]

        for key in self.total_points.keys():
            if self.total_points[key]==winner_points:
                winner.append(key)
        #print(winner_points)
        #print(winner)

        print('~'*80)
        print('\t'*3,'SCORE BOARD')
        for i in self.set.keys():
            print('\nPlayer ',i,' : ',self.player_names[i])
            print('\tTiles left: ',self.set[i])
            print('\tPoints gained in the current round: ',self.cur_points[i])
            print('\tTotal points: ',self.total_points[i])

        if winner_points >= 25:

            if len(winner)==1:
                print('\n\t','*'*50)
                print('\t\tCONGRATULATIONS ',self.player_names[winner[0]],'!!')
                print('\t\tYOU ARE THE WINNER!!!')
                print('\n\t','*'*50)
                print('\n','~'*80)
                s=input('Press any key to continue...')
                return -1
            else:
                print('\t\tITS A DRAW!!!')
                print('\t\tBETWEEN PLAYERS ',end='\t')
                for w in winner:
                    print(self.player_names[w],end='\t')
                print('\nThe Game continues...')
                print('\n','~'*80)
                s=input('Press any key to continue...')
                return 1    #play again

        else:
            print('\nNo player scored points >= 25...')
            print('The Game continues...')
            print('\n','~'*80)
            s=input('Press any key to continue...')
            return 1    #play again

def Dom_heading():
    print('='*100)
    print('\t'*5,'D O M I N O E Z')
    print('='*100)

class all_functions:

    def about(self):
        print('\nDominoes is a family of tile-based games played with rectangular "domino" tiles. Each domino is a rectangular tile with a line'
              'dividing its face into two square ends. Each end is marked with a number of spots (also called pips, nips, or dobs) or is blank. The '
              'backs of the dominoes in a set are indistinguishable, either blank or having some common design. The domino gaming pieces (colloquially '
              'nicknamed bones, cards, tiles, tickets, stones, chips, or spinners[dubious – discuss]) make up a domino set, sometimes called a deck or '
              'pack.The traditional Sino-European domino set consists of 28 dominoes, featuring all combinations of spot counts between zero and six. '
              'A domino set is a generic gaming device, similar to playing cards or dice, in that a variety of games can be played with a set.')

    def help_rules(self):
        print('\t'*4,'DOMINOES - BLOCKING GAME - RULES')
        print('\nSETUP:')
        print('Type of Dominoes Used: Double 6')
        print('Number of dominoes drawn: For 2 to 4 players, each player draws 7 tiles. If there are any remaining tiles after the draw, they are discarded.')
        print('\nGAMEPLAY:')
        print('Each player tries to match the pips (dots) on one end of a tile from his hand with the pips on an open end of any tile in the layout.',
              'If a player is unable to match a tile from his hand with a tile in the layout, the player passes his turn.',
              'Each player may play only one tile per turn. The first player to get rid of all dominoes wins the game. If none of the players',
              'can make a play, the game ends in a block.')
        print('\nSCORING:')
        print('The player with the lightest hand (i.e. the number of dots on their dominoes) wins the number of sum total of points in all of',
              'his opponents’ hands, minus the points in his own hand. If there is a tie, the win goes to the player with the lightest individual tile.',
              'For example, if one player has a 1-2, 2-4, and 3-5, and the other player has a 5-5 and a 3-4, they both have a total of 17, but the first',
              'player wins because his lightest tile (1-2) is smaller than the second player\'s lightest tile (3-4).',
              'Games are often played in a number of rounds, where the score in each individual round (or hand) is added to the score in the previous',
              'rounds. When one player\'s total score exceeds a pre-established "winning score" (25, for example), the game is over and the winner declared.')

    def quit(self):
        exit()

    def play_main(self,num,comp):
        play_again=1
        lop=LineOfPlay(num,comp)   #2 for 2 players

        while play_again==1:

            lop.reset()
            #lop.create_doublesix()
            #lop.create_play_tiles()
            #lop.distribute()

            #print(lop.points)
            block_res=[]
            game_over=-1
            end_game=0

            #for rounds in range(7):
            while game_over != 1:
                for pno in range(1,lop.no_players+1):   #for each player
                    success=-1
                    print('\n',lop.player_names[pno],', Your Turn')
                    if comp==0 or (comp==1and pno==1):
                        lop.display_tiles(pno)
                        print('You can choose from:')

                    while success == -1:
                        block,ch=lop.choose_tile(pno,comp)
                        block_res.append(block)
                        if block == 1:
                            if comp==0 or (comp==1and pno==1):
                                ch=int(input('Choose(index no - starting from 0): '))
                            success=lop.playing(pno,ch,comp)
                        else:
                            print('You are blocked..You have to pass')
                            if comp==0 or (comp==1and pno==1):
                                x=input('Press any key to continue the game...')
                            success=1

                    print('\n')
                    print('----------'*len(lop.playlist))
                    print("NOW THE LINE OF PLAY:\n ",lop.playlist)
                    print('----------'*len(lop.playlist))

                    #print('block results: ',block_res)
                    if lop.tiles_empty(pno)==1:
                        end_game=1
                    if lop.check_block(block_res)== 1 :
                        end_game=2

                    if end_game==1 or end_game==2:
                        print('\nGAME OVER!!!')
                        game_over=1
                        play_again=lop.calc_points_winner(pno,end_game)   #end_game=1 for tiles empty, =2 for continous block
                        os.system('cls')
                        Dom_heading()
                        break


def main():

    cont='y'
    while cont=='y' or cont=='Y':
        os.system('cls')
        Dom_heading()
        dom=all_functions()
        print('1. ABOUT THE GAME\n2. PLAY\n3. HELP\n4. EXIT')
        choice=int(input('ENTER CHOICE: '))

        if choice==1:
            os.system('cls')
            Dom_heading()
            dom.about()

        elif choice==2:
            #the game
            start=1
            while start==1:
                os.system('cls')
                Dom_heading()
                comp=0
                print('How many players? ')
                print('\t1   : Against Computer')
                print('\t2-4 : Two-Four players')
                num=int(input('Enter : '))
                if num==1:
                    comp=1

                if num in range(1,5):
                    dom.play_main(num,comp)
                    start=0
                else :
                    print('\nINVALID NUMBER OF PLAYERS!!')
                    q=input('Press any key to continue..')
                    start=1

        elif choice==3:
            os.system('cls')
            Dom_heading()
            dom.help_rules()

        else:
            dom.quit()

        cont=input('\nGO BACK TO MAIN MENU (y/n) ? ')

    print('\n')
    print('~'*100)

main()
