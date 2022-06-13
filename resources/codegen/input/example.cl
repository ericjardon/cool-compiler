class Main inherits IO{
 x: Int <- 199;
 main(): Object {{ 
        if ((x) < 200) then {
            x <- 1;
            "verdadero";
        }
        else  {
            x <- 0;
            "falso";
        }
        fi;
    }};
};