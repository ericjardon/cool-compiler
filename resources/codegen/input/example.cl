-- A let-bound variable can shadow a same-named let-bound variable.
class Example inherits Main {
  y:Int;
  
  do(num:Int) : Object {{
    y<-15;
    98;
    let extra:Bool, exxtra:Bool in
      {extra;
      exxtra;
      num;};
  }};
};

class Main inherits IO
{
  x: Int <- 13;
  ex: Example;
  main() : Object {{
    -- ex <- NEW Example; 
    let local:Int<-0 in
      ex.do(local);
  }};
};
