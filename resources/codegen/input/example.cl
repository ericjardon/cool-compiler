-- A let-bound variable can shadow a same-named let-bound variable.


class Main inherits IO
{
  x : Int;

  sub() : Object {
    {
      x <- 44;
      let var : String, var2 : Int <- 18 in
	    {      
        let var3 : Int <- var2 + 74 in
	      var3;
      };
    }
  };

  main() : Object
  {
    x <- 13+14+15
  };
};
