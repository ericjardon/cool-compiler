class Main inherits IO{
 i: Int <- 0;
 main(): Object {{ 
        
        while (i < 5) loop i <- i + 1 pool.type_name();
    }};
};