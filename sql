

SELECT t.*
FROM pacientes_paciente t
JOIN (
    SELECT nombre, fechanacimiento, domicilio, telefono, COUNT(*) AS cantidad
    FROM pacientes_paciente
    GROUP BY nombre, fechanacimiento
    HAVING COUNT(*) > 1
) d

ON t.nombre = d.nombre
AND t.fechanacimiento = d.fechanacimiento
AND t.domicilio = d.domicilio
AND t.telefono = d.telefono;







UPDATE pacientes_paciente
SET telefono = REPLACE(telefono, '"', '')


UPDATE pacientes_paciente
SET domicilio = REPLACE(domicilio, '"', '')


UPDATE pacientes_paciente
SET telefono = SUBSTR(telefono, 2)
WHERE telefono LIKE ' %';

