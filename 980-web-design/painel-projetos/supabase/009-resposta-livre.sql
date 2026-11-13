-- Resposta livre nas decisões: além dos botões, o campo de digitação ganha um botão de envio, para responder algo que não é uma das letras.
-- Rodar uma vez no SQL Editor do projeto <projeto-supabase>, depois do 007-decisoes.sql.
--
-- O botão "enviar" do campo: com letra escolhida, reenvia a letra com o texto (já funcionava pelo 007);
-- sem letra, grava escolha = 'LIVRE' com o texto em ajuste. O propagar-decisoes.py leva como "resposta livre do operador".

alter table public.decisoes_escolhas drop constraint if exists decisoes_escolhas_escolha_check;
alter table public.decisoes_escolhas add constraint decisoes_escolhas_escolha_check check (escolha in ('A', 'B', 'C', 'LIVRE'));
alter table public.decisoes_escolhas drop constraint if exists decisoes_livre_tem_texto;
alter table public.decisoes_escolhas add constraint decisoes_livre_tem_texto check (escolha <> 'LIVRE' or ajuste is not null);
