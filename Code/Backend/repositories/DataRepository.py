from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def add_melding(tijd_melding, tijd_afdrukken_melding, bericht, status_melding):
        sql = "INSERT INTO historiek_melding(tijd_melding, tijd_afdrukken_melding, bericht, status_melding) VALUES(%s,%s,%s,%s)"
        params = [tijd_melding, tijd_afdrukken_melding,
                  bericht, status_melding]
        return Database.execute_sql(sql, params)

    @staticmethod
    def get_meldingen():
        sql = "SELECT tijd_melding, (tijd_afdrukken_melding - tijd_melding) as 'reactie_tijd', bericht, status_melding from historiek_melding ORDER BY volgnummer_melding DESC LIMIT 25"
        return Database.get_rows(sql)

    @staticmethod
    def get_status_melding():
        sql = "SELECT * FROM historiek_devices WHERE id_device = 2 ORDER BY datum_meting DESC LIMIT 1"
        return Database.get_one_row(sql)

    @staticmethod
    def get_melding():
        sql = "SELECT * from historiek_melding ORDER BY volgnummer_melding DESC LIMIT 1;"
        return Database.get_one_row(sql)

    @staticmethod
    def update_afdrukken_melding(tijd_afdrukken_melding, volgnummer_melding):
        sql = "UPDATE historiek_melding SET tijd_afdrukken_melding = %s WHERE volgnummer_melding = %s"
        params = [tijd_afdrukken_melding, volgnummer_melding]
        return Database.execute_sql(sql, params)

    @staticmethod
    def get_sensorhistoriek():
        sql = "SELECT d.naam, h.datum_meting, h.meetresultaat, d.meeteenheid from historiek_devices h JOIN devices d ON d.id_device = h.id_device WHERE h.id_device = 1 ORDER BY h.datum_meting DESC LIMIT 25"
        return Database.get_rows(sql)

    @staticmethod
    def add_sensorwaarde(id_device, datum_meting, meetresultaat):
        sql = "INSERT INTO historiek_devices(id_device, datum_meting, meetresultaat) VALUES(%s,%s,%s)"
        params = [id_device, datum_meting,
                  meetresultaat]
        return Database.execute_sql(sql, params)

    @staticmethod
    def get_luchtkwaliteit():
        sql = "SELECT * FROM historiek_devices WHERE id_device = 1 ORDER BY datum_meting DESC LIMIT 25"
        return Database.get_rows(sql)

    @staticmethod
    def update_status_device(status_device, id_device):
        sql = "UPDATE devices SET status_device = %s WHERE id_device = %s"
        params = [status_device, id_device]
        return Database.execute_sql(sql, params)

    @staticmethod
    def get_id_device(naam):
        sql = "SELECT id_device from devices WHERE naam = %s"
        params = [naam]
        return Database.get_one_row(sql, params)

    def get_bureau_activiteit():
        sql = "SELECT * FROM historiek_devices WHERE id_device = 3 ORDER BY datum_meting DESC LIMIT 1"
        return Database.get_one_row(sql)

    @staticmethod
    def update_kamer_naam(naam):
        sql = "UPDATE kamer SET voornaam = %s WHERE id_kamer = 1"
        params = [naam]
        return Database.execute_sql(sql, params)

    @staticmethod
    def get_kamer():
        sql = "SELECT * FROM kamer WHERE id_kamer = 1"
        return Database.get_one_row(sql)
