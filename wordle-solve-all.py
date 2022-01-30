import collections
import pprint

answers = [ w.strip() for w in open( 'wordle-answers-alphabetical.txt', 'r' ).readlines() ]
guesses = [ w.strip() for w in open( 'wordle-allowed-guesses.txt', 'r' ).readlines() ]

def match( w, v ):
    p = list(w)
    q = list(v)
    r = ['_'] * 5

    for i in range(5):
        if p[i] == q[i]:
            r[i] = 'G'
            q[i] = '_'

    for i in range(5):
        if r[i] == '_':
            try:
                j = q.index(p[i])
                r[i] = 'Y'
                q[j] = 0
            except:
                pass
    return ''.join(r)
    
def dump_tree( tree ):
    for k, v in tree.items():
        print( 'Guess is', k )
        i = v.items()
        for kkk, vvv in i: print( kkk, len( vvv ), vvv )
        print( max( [ len(x) for _, x, in i ] ), k )
        print()

def make_tree( guesses, answers ):
    m = {}
    for w in guesses:
        n = collections.defaultdict( list )
        for v in answers:
            k = match( w, v )
            n[k].append( v )
        m[w] = dict( n )
    return dict( m )


def find_best_guess( tree ):
    g = []
    for k, v in tree.items():
        ls = []
        for _, x in v.items():
            ls.append( len(x))
        g.append(( max( ls ), k ))
    g.sort()
    return g[0]

# guesses = [ g for g in guesses if g.startswith('a') ]
# answers = [ a for a in answers if a.startswith('a') ]

if __name__ == '__main__':
    import copy
    tree = make_tree( guesses, answers )
    for target in answers:
        # print( target )
        ans = answers[:]
        t = copy.deepcopy( tree )
        c = 0
        while len(ans) > 1:
            c += 1
            count, guess = find_best_guess( t )
            score = match( guess, target )
            ans = t[guess][score]
            # print( count, guess, score, ans, c )
            t = make_tree( guesses, ans )
        print( c, target )