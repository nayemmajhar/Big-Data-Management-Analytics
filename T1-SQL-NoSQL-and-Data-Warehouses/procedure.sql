DECLARE
	startdate date := to_date('2000-01-01','YYYY-MM-DD');
	enddate   date := to_date('2039-12-31','YYYY-MM-DD');
	currdate  date := startdate;
	counter   int  := 1;  -- current DSid
BEGIN
	DELETE FROM Facttab;
	DELETE FROM DCustomer;
	DELETE FROM DProduct;
	DELETE FROM DDate;
	
	COMMIT ;
	
	DROP SEQUENCE IF EXISTS Facttab_ID;
	DROP SEQUENCE IF EXISTS DCustomer_Sid;
	DROP SEQUENCE IF EXISTS DProduct_Sid;
	
	CREATE SEQUENCE Facttab_ID
		INCREMENT BY 1 
		START WITH 1;

	CREATE SEQUENCE DCustomer_Sid
		INCREMENT BY 1 
		START WITH 1;

	CREATE SEQUENCE DProduct_Sid
		INCREMENT BY 1 
		START WITH 1;
	
	COMMIT;
	
	WHILE currdate <= enddate LOOP
		INSERT INTO
		DDate(DSid, SalesDate, Day, Week, WeekInYear, Month,
			   MonthInYear, Monthname, Quarter, QuarterInYear, Year)
		VALUES (counter,
				currdate,
				CAST (to_char(currdate,'DD') AS Smallint), 
				CAST (to_char(currdate,'YYYYIW') AS INTEGER),
				CAST (to_char(currdate,'IW') AS Smallint),
				CAST (to_char(currdate,'YYYYMM') AS INTEGER),
				CAST (to_char(currdate,'MM') AS Smallint),
				to_char(currdate,'MONTH'),
				CAST (to_char(currdate,'YYYYQ') AS INTEGER), 
				CAST (to_char(currdate,'Q') AS Smallint), 
				CAST (to_char(currdate,'YYYY') AS INTEGER) 
		);
		currdate := currdate + 1;
		counter  := counter + 1;
	END LOOP;
	
	COMMIT;
	
	-- Filling of the dimension DCustomer:
	
	INSERT INTO DCustomer(CSid, CustId, Name, Place, State, Country)
	SELECT nextval('DCustomer_Sid'), CID, Name, Place, NULL, trim(to_char(ZIP,'09999'))
	From Customer   ; 

	UPDATE DCustomer
	SET State = 'Sachsen'
	WHERE Substr(Country, 1, 2) IN ('01','02','04','08','09');

	UPDATE DCustomer
	SET State = 'Brandenburg'
	WHERE Substr(Country, 1, 2) IN ('03','14','15','16');

	UPDATE DCustomer
	SET State = 'Sachsen-Anhalt'
	WHERE Substr(Country, 1, 2) IN ('06','39');

	UPDATE DCustomer
	SET State = 'Thüringen'
	WHERE Substr(Country, 1, 2) IN ('07','98','99');

	UPDATE DCustomer
	SET State = 'Berlin'
	WHERE Substr(Country, 1, 2) IN ('10','12','13');

	UPDATE DCustomer
	SET State = 'Mecklenburg-Vorpommern'
	WHERE Substr(Country, 1, 2) IN ('17','18','19');

	UPDATE DCustomer
	SET State = 'Hamburg'
	WHERE Substr(Country, 1, 2) IN ('20','22');

	UPDATE DCustomer
	SET State = 'Niedersachsen'
	WHERE Substr(Country, 1, 2) IN ('21','26','27','29','30','31','37','38','49');

	UPDATE DCustomer
	SET State = 'Bremen'
	WHERE Substr(Country, 1, 2) IN ('28');

	UPDATE DCustomer
	SET State = 'Nordrhein-Westfalen'
	WHERE Substr(Country, 1, 2) IN ('32','33','40','41','42','43','44','45','46','47','48','50','51','52','53','58','59');

	UPDATE DCustomer
	SET State = 'Schleswig-Holstein'
	WHERE Substr(Country, 1, 2) IN ('23','24','25');

	UPDATE DCustomer
	SET State = 'Hessen'
	WHERE Substr(Country, 1, 2) IN ('34','35','36','60','61','63','64','65');

	UPDATE DCustomer
	SET State = 'Rheinland-Pfalz'
	WHERE Substr(Country, 1, 2) IN ('54','55','56','57','67');

	UPDATE DCustomer
	SET State = 'Saarland'
	WHERE Substr(Country, 1, 2) IN ('66');

	UPDATE DCustomer
	SET State = 'Baden-Württemberg'
	WHERE Substr(Country, 1, 2) IN ('68','69','70','71','72','73','74','75','76','77','78','79','88');

	UPDATE DCustomer
	SET State = 'Bayern'
	WHERE Substr(Country, 1, 2) IN ('80','81','82','83','84','85','86','87','89','90','91','92','93','94','95','96','97');

	UPDATE DCustomer
	SET Country = 'Germany'
	WHERE State IS NOT NULL;

	UPDATE DCustomer
	SET Country = 'Foreign Country'
	WHERE State IS NULL;

	-- Filling of the dimension DProduct:

	INSERT INTO DProduct(PSid, ArtId, Name, ProdgrId, Prodgroup, Color, Price)
	SELECT nextval('DProduct_Sid'), AId, Name, NULL, NULL, Color, Price
	FROM Article   ;

	UPDATE DProduct
	SET Prodgroup = 'Man bicycle', ProdgrID = 100
	WHERE Upper(Name) LIKE 'MAN%BIKE%';

	UPDATE DProduct
	SET Prodgroup = 'Lady bicycle', ProdgrID = 200
	WHERE Upper(Name) LIKE 'WOMAN%BIKE%';

	UPDATE DProduct
	SET Prodgroup = 'Juvenile bicycle', ProdgrID = 300
	WHERE Upper(Name) LIKE 'JUVENILE%BIKE%';

	UPDATE DProduct
	SET Prodgroup = 'Mountainbike', ProdgrID = 400
	WHERE Upper(Name) LIKE 'MOUNTAINBIKE%';

	UPDATE DProduct
	SET Prodgroup = 'Equipment', ProdgrID = 500
	WHERE ArtId > 500000;

	UPDATE DProduct
	SET Prodgroup = 'Intermediate product', ProdgrID = 600
	WHERE ArtId Between 200000 And 500000;

	-- Filling of Facttab:

	INSERT INTO Facttab (FId, PSid, CSid, DSid, Price, Quantity)
	SELECT nextval('Facttab_ID'), PSid, CSid, DSid, Totalprice/Quantity, Quantity
	FROM Orders NATURAL INNER JOIN Orderposition
					 INNER JOIN DDate ON OrderDate = SalesDate
					 INNER JOIN DCustomer USING (CustId)
					 INNER JOIN DProduct USING (ArtId)   ;
	COMMIT;
	
END;