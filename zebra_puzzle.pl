/* -*- Mode:Prolog; coding:iso-8859-1; indent-tabs-mode:nil; prolog-indent-width:8; prolog-paren-indent:4; tab-width:8; -*- 
Constraint store

Author: Tony Lindgren

*/
:- use_module([library(clpfd)]).

zebra:-
        % Define variabels and their domain      
        House_colors = [Red, Green, White, Yellow, Blue],
        domain(House_colors, 1, 5),
        Pet = [Dog, Birds, Cats, Horse, Zebra], 
        domain(Pet, 1, 5),
        Smokes = [Pall_mall, Dunhill, Blend, Prince, Blue_master],
        domain(Smokes, 1, 5),  
        Drinks = [Tea, Coffee, Milk, Beer, Water],
        domain(Drinks, 1, 5),
        Nationality =[English, Swede, Dane, Norwegian, German],  
        domain(Nationality, 1, 5),
       
        % Define constraints and relations
        all_different(House_colors),
        all_different(Pet),
        all_different(Smokes),
        all_different(Drinks),
        all_different(Nationality),       
        Red #= English,  
        Swede #= Dog,  
        Dane #= Tea,
        Green #= White - 1, 
        Pall_mall #= Birds,
        Yellow #= Dunhill,
        Milk #= 3,
        Norwegian #= 1,
        Blend #= Cats +1 #\/ Blend #= Cats - 1,
        Dunhill #= Horse + 1 #\/ Dunhill #= Horse - 1,
        Blue_master #= Beer,
        German #= Prince,
        Norwegian #= Blue + 1 #\/ Norwegian #= Blue -1,
        Water #= Blend + 1 #\/ Water #= Blend - 1,
        
        
        % append variables to one list
        append(House_colors, Nationality, Temp1),
        append(Temp1, Pet, Temp2),
        append(Temp2, Drinks, Temp3),
        append(Temp3, Smokes, VariableList),
        
        % find solution
        labeling([], VariableList),                                           
       
        % connect answers with right objects
        sort([Red-red, Green-green, White-white, Yellow-yellow, Blue-blue], House_color_connection),
        sort([English-english, Swede-swede, Dane-dane, Norwegian-norwegian, German-german], Nation_connection),
        sort([Dog-dog, Birds-birds, Cats-cats, Horse-horse, Zebra-zebra], Pet_connection),
        sort([Pall_mall-pall_mall, Dunhill-dunhill, Blend-blend, Prince-prince, Blue_master-blue_master], Smokes_connection ),
        sort([Tea-tea, Coffee-coffee, Milk-milk, Beer-beer, Water-water], Drinks_connection ),      
       
        % print solution
        Format = '~w~15|~w~30|~w~45|~w~60|~w~n',
        format(Format, ['house 1', 'house 2', 'house 3', 'house 4', 'house 5']),
        format(Format, House_color_connection),
        format(Format, Nation_connection),  
        format(Format, Smokes_connection),  
        format(Format, Drinks_connection),  
        format(Format, Pet_connection).                                                        

            
        