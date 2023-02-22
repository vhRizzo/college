library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity ula is

	port(
		A, B											:	in		unsigned   		  (3 downto 0);
		PB1, PB2										:	in		std_logic;
		R									 			:	out 	unsigned   		  (4 downto 0);
		DSSa, DSSb, DSSc, DSSd, DSSe, DSSf	:	out	std_logic_vector (6 downto 0)
	);
	
end entity ula;

architecture main of ula is

begin

	process (PB1)
	
		variable Atemp			: unsigned (4 downto 0);
		variable Btemp			: unsigned (4 downto 0);
		variable Temp4b		: unsigned (3 downto 0);
		variable Temp5b		: unsigned (4 downto 0);
		variable AritDez		: integer;
		variable AritUni		: integer;
		variable Op				: integer := 0;
		
		begin
			
			Temp5b := "00000";
		
			Atemp(4) := '0';
			Atemp(3 downto 0) := A;
			
			Btemp(4) := '0';
			Btemp(3 downto 0) := B;
			
			if (rising_edge(PB1)) then
				Op := Op + 1;
			end if;
				
			if (Op >= 6) then
				Op := 0;
			end if;
			
			if (Op = 0) then
				Temp5b := Atemp + Btemp;
				AritDez := to_integer(Temp5b) rem 10;
				AritUni := to_integer(Temp5b) - AritDez;
				
			elsif (Op = 1) then
				if (Atemp >= Btemp) then
					Temp5b := Atemp - Btemp;
					AritDez := to_integer(Temp5b) rem 10;
					AritUni := to_integer(Temp5b) - AritDez;
				else
					Temp5b := Btemp - Atemp;
					AritDez := to_integer(Temp5b) rem 10;
					AritUni := to_integer(Temp5b) - AritDez;
					Temp5b(4) := '1';
				end if;
				
			elsif (Op = 2) then
				Temp5b(4) := '0';
				Temp4b := A and B;
				Temp5b(3 downto 0) := Temp4b;
				
			elsif (Op = 3) then
				Temp5b(4) := '0';
				Temp4b := A or B;
				Temp5b(3 downto 0) := Temp4b;
				
			elsif (Op = 4) then
				Temp5b(4) := '0';
				Temp4b := A xor B;
				Temp5b(3 downto 0) := Temp4b;
				
			elsif (Op = 5) then
				Temp5b(4) := '0';
				Temp4b := not A;
				Temp5b(3 downto 0) := Temp4b;
				
			end if;
			
			case Op is
					
				when 0 => 
					DSSf <= "1000000"; --'0'
					DSSe <= "0001000"; --'A'
				when 1 => 
					DSSf <= "1111001"; --'1'
					DSSe <= "0010010"; --'S'
				when 2 =>
					DSSf <= "0100100"; --'2'
					DSSe <= "0001000"; --'A'
				when 3 =>
					DSSf <= "0110000"; --'3'
					DSSe <= "1000000"; --'O'
				when 4 =>
					DSSf <= "0011001"; --'4'
					DSSe <= "0001001"; --'X'
				when 5 =>
					DSSf <= "0010010"; --'5'
					DSSe <= "1000110"; --'C'
				when others => DSSf <= "0000110"; --'E'
					
			end case;
			
			if (PB2 = '0') then
			
				R <= Temp5b;
				
				DSSe <= "1111111";
				DSSd <= "1111111";
				DSSc <= "1111111";
				
				if (Op = 0 or Op = 1) then
				
					case AritUni is
                    
						when 0 => DSSa <= "1000000"; --'0'
						when 1 => DSSa <= "1111001"; --'1'
						when 2 => DSSa <= "0100100"; --'2'
						when 3 => DSSa <= "0110000"; --'3'
						when 4 => DSSa <= "0011001"; --'4'
						when 5 => DSSa <= "0010010"; --'5'
						when 6 => DSSa <= "0000010"; --'6'
						when 7 => DSSa <= "1111000"; --'7'
						when 8 => DSSa <= "0000000"; --'8'
						when 9 => DSSa <= "0010000"; --'9'
						when others => DSSa <= "0000110"; --'E'

					end case;

					case AritDez is
                    
						when 0 => DSSb <= "1000000"; --'0'
						when 1 => DSSb <= "1111001"; --'1'
						when 2 => DSSb <= "0100100"; --'2'
						when 3 => DSSb <= "0110000"; --'3'
						when 4 => DSSb <= "0011001"; --'4'
						when 5 => DSSb <= "0010010"; --'5'
						when 6 => DSSb <= "0000010"; --'6'
						when 7 => DSSb <= "1111000"; --'7'
						when 8 => DSSb <= "0000000"; --'8'
						when 9 => DSSb <= "0010000"; --'9'
						when others => DSSa <= "1111111"; --'apagado'

					end case;
					
					if (Op = 1 and Temp5b(4) = '1') then
						DSSc <= "0111111";
					end if;
					
				else
				
					case Temp5b(0) is
					
						when '0' => DSSa <= "1000000"; --'0'
						when '1' => DSSa <= "1111001"; --'1'
						
					end case;
					
					case Temp5b(1) is
					
						when '0' => DSSb <= "1000000"; --'0'
						when '1' => DSSb <= "1111001"; --'1'
						
					end case;
					
					case Temp5b(2) is
					
						when '0' => DSSc <= "1000000"; --'0'
						when '1' => DSSc <= "1111001"; --'1'
						
					end case;
					
					case Temp5b(3) is
					
						when '0' => DSSd <= "1000000"; --'0'
						when '1' => DSSd <= "1111001"; --'1'
						
					end case;
					
					case Temp5b(4) is
					
						when '0' => DSSe <= "1000000"; --'0'
						when '1' => DSSe <= "1111001"; --'1'
						
					end case;
					
				end if;
	
			end if;
				
	end process;
		
end architecture main;
