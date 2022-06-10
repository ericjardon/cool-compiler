class Main inherits IO
{
  main() : Object
  {
    let thing : Object <- self in
      case thing of
        o : Object => out_string( "is object\n" );
	      m : Main => out_string( "is main\n" );
      esac
  };
};
