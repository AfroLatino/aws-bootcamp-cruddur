-- this file was manually created
INSERT INTO public.users (display_name, email, handle, cognito_user_id)
VALUES
  ('AfroLatino', 'afrolatino@test.com','AfroLatino' ,'MOCK'),
  ('londo', 'lmollari@centari.com','londo' ,'MOCK'),
  ('Andrew Brown', 'andrewb@exampro.co','andrewbrown' ,'MOCK');


INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'Afrolatino' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  ),
  (
    (SELECT uuid from public.users WHERE users.handle = 'londo' LIMIT 1),
    'I am the other!',
    current_timestamp + interval '10 day'
  );