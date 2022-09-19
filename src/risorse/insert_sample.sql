BEGIN TRANSACTION;

-- psql -U <user> -d <db> -f risorse/insert_sample.sql 
insert into documento (id, nome, descrizione, href) values (1, 'voucher', 'voucher gadget fiera UNIBAS', '"voucher" => <path to HOME>/flask-georest/pdf_sample/voucher.pdf');
insert into documento (id, nome, descrizione, href) values (2, 'no voucher', 'voucher gia scaricato', '"no-voucher" => <path to HOME>/flask-georest/pdf_sample/no-voucher.pdf');

-- postgis 3.0.0 fa il parsing delle geometrie in SRID=4326 se non è specificato altro
insert into posizione values (1, 'Italia', 'Lazio', 'Rome', 'Posizione Fiera', ST_GeomFromGeoJSON('{ "type": "Polygon",
        "coordinates": [
          [
          ]]}'),ST_GeomFromGeoJSON('{ "type": "Polygon",
        "coordinates": [
          [

        ]]}'));

-- voucher in fiera
insert into accesso values (1, 1, 1);
-- no voucher in fiera
insert into accesso values (2, 2, 1);

COMMIT;
