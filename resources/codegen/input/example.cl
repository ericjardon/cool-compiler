-- A let-bound variable can shadow a same-named let-bound variable.
class Example inherits Main {
  y:Int;
  do() : Object {{
    y<-15;
  }};
};

class Main inherits IO
{
  x: Int;
  ex: Example;
  main() : Object {{
    ex <- NEW Example; 
    ex.do();
  }};

};
