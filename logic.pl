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
% We need to to find how complex the term is.
% recursive is a good way to do and have 2 stops when the conditions are fullfilled.
% Ad a temporary counter in the middle that ads upp when terms apply and then copy to the variable Complexity at the end (Hide complexity during proces)

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
        % Check if an operator can be utilized or not  // titta om precondtions för op är uppfylda
        % your_name(Preconditions, State)
        subset(Preconditions, State),
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Define a predicate that becomes true if:  %% Question to Tony do you mean a predicate here or can i use m_member just to check? Is Yes and No considered true/false?
        %       all members of Preconditions are part of current State (State) 
        % and return false otherwise
        m_member(Preconditions, Sofar),
    
        % Test to avoid using the operator multiple times %% What should this do? Is this correct?
        % (To avoid infinite loops, in more comlex problems this is often implemented via states)
        % your_name(Op, Sofar)
        m_member(Op, Sofar),
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Define a predicate that checks if Op has been done before %% Is this a part of the assignment above? How to break a loop if part of it?
        % if so the predicate should fail otherwise be true 
        
        % First half of applying an operator  %% Is this with the things bellow? or is this a separete one, if so what is the one bellow?
        % your_name(State, Delete, Remainder),
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Define a predicate that removes all members of the Delete list 
        % from the state and the results are returned in the Reminder 
        diff(State, Delete, Remainder),
        append(Add, Remainder, NewState),
        % Useful for debugging (de-comment to see output) 
        %format('Operator:~w ~N', [Op]),    
        %format('NewState:~w ~N', [NewState]),
        solve(NewState, Goal, [Op|Sofar], Plan).

solve(State, Goal, Plan, RPlan):-
        %add a check if State is a subset of Goal here 
        subset(State,Goal),
        reverse(Plan,RPlan).

%reverse(Plan,RPlan) - define this predicate which returns a reversed list
reverse([], Z, Z).
reverse([X|Y], Z, W):-
        reverse(Y, Z, [X| W]).
        

        
% The operators take 4 arguments
% 1st arg = name
% 2nd arg = preconditions
% 3rd arg = delete list
% 4th arg = add list.

%op(swing(stick) - define this operator
op(swing(stick),
        [on(monkey,box), at(box, X), at(bananas, X), holding(monkey,stick)],
        [on(monkey,box), holding(monkey,stick)],
        [at(bananas, floor), at(monkey, floor)]).

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
        [at(monkey,X), at(box,X), on(monkey,floor),(box,floor)],
        [at(monkey,X), at(box,X)],
        [at(monkey,Y), at(box,Y)]).

op(go(X,Y),
        [at(monkey,X), on(monkey,floor)],
        [at(monkey,X)],
        [at(monkey,Y)]):- 
        X \== Y.
