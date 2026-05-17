-- Ejecuta en Supabase → SQL Editor (después de supabase_chat_privado.sql)
-- Fotos temporales en el chat (expiran solas en la app tras 24 h)

ALTER TABLE mensajes_chat
ADD COLUMN IF NOT EXISTS imagen_url TEXT;

ALTER TABLE mensajes_chat
ADD COLUMN IF NOT EXISTS expira_at TIMESTAMPTZ;

-- Bucket público para las fotos del chat
INSERT INTO storage.buckets (id, name, public, file_size_limit)
VALUES ('chat-fotos', 'chat-fotos', true, 5242880)
ON CONFLICT (id) DO UPDATE SET public = true, file_size_limit = 5242880;

-- Políticas: la app usa la clave anon
DROP POLICY IF EXISTS "chat_fotos_subir" ON storage.objects;
DROP POLICY IF EXISTS "chat_fotos_ver" ON storage.objects;

CREATE POLICY "chat_fotos_subir"
ON storage.objects FOR INSERT TO anon
WITH CHECK (bucket_id = 'chat-fotos');

CREATE POLICY "chat_fotos_ver"
ON storage.objects FOR SELECT TO anon
USING (bucket_id = 'chat-fotos');
