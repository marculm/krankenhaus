DROP INDEX IF EXISTS
    krankenhaus_name_idx,
    adresse_plz_idx,
    adresse_krankenhaus_id_idx,
    fachbereich_name_idx,
    fachbereich_krankenhausid_idx;

DROP TABLE IF EXISTS
    fachbereich,
    adresse,
    krankenhaus;
