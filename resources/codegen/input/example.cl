-- A let-bound variable can shadow a same-named let-bound variable.
class Example inherits Main {
  y:Int <- 145;
  
  do() : Object {{
    -- y<-15;
    1;
  }};
};

class Main inherits IO
{
  x: Example;
  main():Object {{
      13;
      x.do();
    }};
};
