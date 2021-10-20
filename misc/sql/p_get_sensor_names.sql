/* Select sensor names for a specified network */
CREATE PROCEDURE PROC_GET_SENSOR_NAMES (@networkID as INT, @sensorName as NVARCHAR(MAX) OUTPUT)
AS
BEGIN
	SET NOCOUNT ON;
	
	SELECT DISTINCT @sensorName = sensorName
	FROM salfordMove.dbo.SENSORS
	WHERE networkID = @networkID
END
GO