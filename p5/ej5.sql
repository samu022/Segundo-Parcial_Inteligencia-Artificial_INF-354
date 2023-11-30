

CREATE PROCEDURE CompararPalabras
    @palabra1 varchar(20),
    @palabra2 varchar(20)
AS
BEGIN
	---****************************************Desde aqui codigo de la clase
    DECLARE @longitud1 int,
            @longitud2 int,
            @posicion int,
            @letra varchar(2),
            @contador int,
            @sql nvarchar(2000),
            @columna varchar(4),
            @contar int,
			@resultado int,
			@exactitud1 float,
			@exactitud2 float
	
    SET @longitud1 = LEN(@palabra1)
    SET @longitud2 = LEN(@palabra2)
	-- DROP TABLE nombre
	DROP TABLE IF EXISTS nombre;
	DROP TABLE IF EXISTS resultado;

    SELECT @posicion = 1
    SELECT @sql = 'CREATE TABLE nombre ('
    WHILE @posicion <= @longitud1
    BEGIN
        SELECT @letra = LEFT(@palabra1, 1)
        SELECT @palabra1 = RIGHT(@palabra1, LEN(@palabra1) - 1)
        SELECT @sql = @sql + @letra + CAST(@posicion AS varchar) + ' int, '
        SELECT @posicion = @posicion + 1
    END
    SELECT @sql = LEFT(@sql, LEN(@sql) - 1)
    SELECT @sql = @sql + ')'
    EXEC sp_executesql @sql

    SELECT @posicion = 1
    WHILE @posicion <= @longitud2
    BEGIN
        SELECT @letra = LEFT(@palabra2, 1)
        SELECT @palabra2 = RIGHT(@palabra2, LEN(@palabra2) - 1)
        SELECT @contar = COUNT(*)
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'nombre'
        AND LEFT(COLUMN_NAME, 1) = @letra
        AND ORDINAL_POSITION <= @posicion
        IF @contar > 0
        BEGIN
            SELECT TOP 1 @columna = COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = 'nombre'
            AND LEFT(COLUMN_NAME, 1) = @letra
            AND ORDINAL_POSITION >= @posicion
            SELECT @sql = 'INSERT INTO nombre(' + @columna + ') VALUES(1)'
            EXEC sp_executesql @sql
        END
        SELECT @posicion = @posicion + 1
    END

    SET @sql = 'SELECT '
    SELECT @contar = COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = 'nombre'
    SELECT @posicion = 1
    WHILE @posicion <= @contar
    BEGIN
        SELECT @columna = COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'nombre' AND ORDINAL_POSITION = @posicion
        SET @sql = @sql + 'SUM(ISNULL(' + @columna + ',0)) +'
        SELECT @posicion = @posicion + 1
    END
    SELECT @sql = LEFT(@sql, LEN(@sql) - 1) + ' FROM nombre'
	EXEC sp_executesql @sql;
	---*********************************************************** HASTA AQUI
    -- Ejecutar la consulta y capturar el resultado de la primera fila en @resultado
	DECLARE @dynamicResult TABLE (Resultado INT);
	INSERT INTO @dynamicResult (Resultado)
	EXEC sp_executesql @sql;

	-- Obtener el resultado de la primera fila
	SELECT TOP 1 @resultado = Resultado FROM @dynamicResult
	-- Comparar con las longitudes de las cadenas
	
	IF @resultado = @longitud1 AND @resultado = @longitud2
	BEGIN
		PRINT 'Las Cadenas son Iguales';
	END
	ELSE
	BEGIN
		PRINT 'Las Cadenas no son iguales';
	END
    
	CREATE TABLE resultado (
		Descripción VARCHAR(255),
		Resultado VARCHAR(255)
	);
	DECLARE @resul VARCHAR(255);
	SET @resul = CONVERT(VARCHAR(255), @resultado);
	--exactitud
	SET @exactitud1 = (CAST(@resultado AS FLOAT) / @longitud1 ) * 100;
	DECLARE @exac1 VARCHAR(255);
	SET @exac1 = CONVERT(VARCHAR(255), @exactitud1);

	SET @exactitud2 = (CAST(@resultado AS FLOAT) / @longitud2) *100; -- Cast @resultado to FLOAT
	
	DECLARE @exac2 VARCHAR(255);
	SET @exac2 = CONVERT(VARCHAR(255), @exactitud2);
	--Insertamos los valoress en la tabla resultado
	Insert into resultado values ('# de caracteres coincidentes: ', @resul);
	IF @resultado = @longitud1 AND @resultado = @longitud2
	BEGIN
		Insert into resultado values ('Resultado: ', 'Las cadenas son iguales');
	END
	ELSE
	BEGIN
		Insert into resultado values ('Resultado: ', 'Las cadenas NO son iguales');
	END
	Insert into resultado values ('Exactitud cadena 1(%): ', @exac1);
	Insert into resultado values ('Exactitud cadena 2(%): ', @exac2);
	Select * from resultado;

END


DROP PROCEDURE IF EXISTS CompararPalabras;


EXEC CompararPalabras @palabra1 = 'arizmendi', @palabra2 = 'arismendi';
EXEC CompararPalabras @palabra1 = 'arismendi', @palabra2 = 'arismendi';
EXEC CompararPalabras @palabra1 = 'hola', @palabra2 = 'halo';
EXEC CompararPalabras @palabra1 = 'abcde', @palabra2 = 'abfde';
EXEC CompararPalabras @palabra1 = 'maria', @palabra2 = 'airam';
EXEC CompararPalabras @palabra1 = 'aaab', @palabra2 = 'aab';
EXEC CompararPalabras @palabra1 = 'lucas', @palabra2 = 'lucas';
