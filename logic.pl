/* -*- Mode:Prolog; coding:iso-8859-1; indent-tabs-mode:nil; prolog-indent-width:8; prolog-paren-indent:4; tab-width:8; -*- 
Logic Assignment
Author: Tony Lindgren
*/

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Part 1: Usage of Knowledgbase
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

belongs_to(harry_potter, gryffindor).
belongs_to(hermione_granger, gryffindor).
belongs_to(cedric_diggory, hufflepuff).
belongs_to(draco_malfoy, slytherin).
wand(harry_potter, '11"_holly_phoenix').
wand(harry_potter, '11"_vine_dragon').
wand(harry_potter, '10"_blackthorn_unknown').
wand(harry_potter, '10"_hawthorn_unicorn').
wand(harry_potter, '15"_elder_thestral_hair').
wand(hermione_granger, '11"_vine_dragon_heartstring').
wand(hermione_granger, '13"_walnut_dragon_heartstring').
wand(cedric_diggory, '12"_ash_unicorn_hair').
wand(draco_malfoy, '10"_hawthorn_unicorn_hair').
wand(draco_malfoy, '15"_elder_thestral_hair').
patronus(harry_potter, stag).
patronus(hermione_granger, otter).
boggart(harry_potter,dementor).
boggart(hermione_granger,failure).
boggart(draco_malfoy,lord_voldemort).
loyalty(harry_potter, gryffindor).
loyalty(harry_potter, hermione_granger).
loyalty(hermione_granger, gryffindor).
loyalty(hermione_granger, harry_potter).
loyalty(cedric_diggory, hufflepuff).
loyalty(cedric_diggory, harry_potter).
influence(harry_potter, hermione_granger).
influence(hermione_granger, harry_potter).
influence(cedric_diggory, hermione_granger).
influence(cedric_diggory, harry_potter).
influence(draco_malfoy, hogwarts).
influence(hogwarts, gryffindor).
influence(hogwarts, slytherin).
influence(hogwarts, hufflepuff).
influence(hogwarts, harry_potter).
influence(hogwarts, hermione_granger).
influence(hogwarts, cedric_diggory).
influence(hogwarts, draco_malfoy).

% trans_influence(X, Y) X influnces Y through some other object Z
trans_influence(X,Y):-  influence(X,Z), influence(Z,Y).
        
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Part 2: Define set and handle terms
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Define predicates to handle sets 
m_member(X,[X|_]).
m_member(X,[_|Y]) :-
        m_member(X,Y).

to_set([],[]).
to_set([X|Y], S):- 
        m_member(X,Y), 
        !, 
        to_set(Y,S).
to_set([X|Y],[X|Z]):-
        to_set(Y,Z).

union(X,Y,Zset):-
        to_set(X, Xset),
        to_set(Y, Yset),
        m_union(Xset,Yset,Zset).
m_union([],Z,Z).
m_union([X|Y],Z,W):-
        m_member(X,Z), 
       % !,
        m_union(Y,Z,W).
m_union([X|Y],Z,[X|W]):-
        \+m_member(X,Z), 
        m_union(Y,Z,W).  

intersection(X,Y,Zset):-
        to_set(X, Xset),
        to_set(Y, Yset),
        m_intersection(Xset, Yset, Zset).
m_intersection([],_,[]).
m_intersection([X|Y],Z,[X|W]) :-
        m_member(X,Z), 
        m_intersection(Y,Z,W).
m_intersection([X|Y],Z,W) :-
        \+ m_member(X,Z), 
        m_intersection(Y,Z,W).

diff(X,Y,Zset):-
        to_set(X,Xset),
        to_set(Y,Yset),
        m_diff(Xset,Yset,Zset).
        
m_diff(X,Y,Z):-
        findall(W,(m_member(W,X),\+(m_member(W,Y))),Z).        


subset([],_).
subset([X|L],K):-
        m_member(X,K), 
        subset(L,K).

% Define predicate that computes the syntactic complexity  


% checks for non variable terms and increases/add 1
len_nv([],0).
len_nv([Head|Tail],N):- nonvar(Head),len_nv(Tail,N1), N is N1+1.
len_nv([Head|Tail],N):- var(Head),len_nv(Tail,N1), N is N1.

syntactic_complexity([], 1).
syntactic_complexity(V, 2):-
       functor(V, _, 0).       % if condition true then 2 returns since only complext term in functor 
syntactic_complexity(V,Complexity) :- 
        nonvar(V), % checks if not variable else unifies and returns 1.exit
        functor(V, _, A),
        V =.. [H|[H2|T2]],write('......'),write(H2),
        len_nv([H|T2],N),
        syntactic_complexity(H2, NX), Complexity is NX+A+N.


%Example outputs
% syntactic_complexity(f(g(h,X),Y),Complexity). is 8
% syntactic_complexity(f(g(H,X),Y),Complexity). is 7
% syntactic_complexity(loyalty(a,N),Complexity) is 5
% syntactic_complexity(loyalty(a,b),Complexity) is 6

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Part 3: Monkey and banana
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This predicate initialises the search for a solution to the problem. 
% The 1st argument of solve/4 is the initial state, 
% the 2nd the goal statepaint,
% the 3rd is a temporary list of actions creating the plan, initially empty 
% the 4th the plan that will be produced.

start(Plan):-   
    solve([on(monkey,floor),on(box,floor),at(monkey,a),at(box,b),
           at(bananas,c),at(stick,d),status(bananas,hanging)],
           [status(bananas,grabbed)], [], Plan).

% This predicate produces the plan. Once the Goal list is a subset 
% of the current State the plan is complete and it is written to 
% the screen using write_sol/1.

solve(State, Goal, Sofar, Plan):-
        op(Op, Preconditions, Delete, Add),
        % Check if an operator can be utilized or not 
        % your_name(Preconditions, State)
        subset(Preconditions, State),
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Define a predicate that becomes true if: 
        %       all members of Preconditions are part of current State (State) 
        % and return false otherwise
        
    
        % Test to avoid using the operator multiple times
        % (To avoid infinite loops, in more comlex problems this is often implemented via states)
        % your_name(Op, Sofar)
        %check_list(Op, Sofar), %% Gör om till wraper så att den kan ta in båda listorna. FIX THIS!!!!
        \+ m_member(Op, Sofar),
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Define a predicate that checks if Op has been done before 
        % if so the predicate should fail otherwise be true 
        
        % First half of applying an operator  
        % your_name(State, Delete, Remainder),
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Define a predicate that removes all members of the Delete list 
        % from the state and the results are returned in the Reminder 
        diff(State, Delete, Remainder),
        append(Add, Remainder, NewState),
        % Useful for debugging (de-comment to see output) 
        format('Operator:~w ~N', [Op]),    
        format('NewState:~w ~N', [NewState]),
        solve(NewState, Goal, [Op|Sofar], Plan).

solve(State, Goal, Plan, RPlan):-
        %add a check if State is a subset of Goal here 
        subset(Goal, State).
        reverse(Plan,RPlan).

%reverse(Plan,RPlan) - define this predicate which returns a reversed list

reverse(X, Y):-
        reverse(X, Y, []).

reverse([], Z, Z).
reverse([X|Y], Z, W):-
        reverse(Y, Z, [X| W]).

check_list([],_).        
check_list([X|Y], Z):-
        check_list(Y, Z), 
        m_member(X, Z).
        
% The operators take 4 arguments
% 1st arg = name
% 2nd arg = preconditions
% 3rd arg = delete list
% 4th arg = add list.

%op(swing(stick) - define this operator
op(swing(stick),
        [on(monkey,box), at(box, X), at(bananas, X), holding(monkey,stick), status(bananas, hanging)],
        [status(bananas, hanging)],
        [status(bananas, grabbed)]).

op(grab(stick),
        [at(monkey,X), at(stick, X), on(monkey,floor)],
        [at(stick, X)],
        [holding(monkey,stick)]).

%op(climbon(box) - define this operator
op(climbon(box),
        [at(monkey,X), at(box,X), on(monkey,floor), on(box,floor)],
        [on(monkey,floor)],
        [on(monkey,box)]).       

%op(push(box,X,Y) - define this operator
op(push(box,X,Y),
        [at(monkey,X), at(box,X), on(monkey,floor), on(box,floor)],
        [at(monkey,X), at(box,X)],
        [at(monkey,Y), at(box,Y)]).

op(go(X,Y),
        [at(monkey,X), on(monkey,floor)],
        [at(monkey,X)],
        [at(monkey,Y)]):- 
        X \== Y.
