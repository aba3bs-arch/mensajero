-- Ejecuta esto en Supabase: SQL Editor → New query → Run
-- Agrega soporte para chats privados entre empleados

ALTER TABLE mensajes_chat
ADD COLUMN IF NOT EXISTS destinatario TEXT;

-- destinatario NULL  = chat general (toda la tienda)
-- destinatario = nombre del empleado = mensaje privado solo para esa persona
