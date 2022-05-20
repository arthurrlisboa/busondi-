from backend.database.config.db_connection import DBConnection
from backend.database.models.route_stop import RouteStop
from backend.database.models.bus_stops import BusStops
from backend.database.models.user import User

class RepositoryImpl:
    def get_all_stops_repo_():
        with DBConnection() as connection:
            all_stops = connection.session.query(BusStops).all()
        return all_stops

    def get_stop_by_id_repo_(stop_id):
        with DBConnection() as connection:
            stop = connection.session.query(BusStops).filter_by(stop_id=stop_id).first()
        return stop

    def get_routes_from_stop_repo_(stop_id):
        with DBConnection() as connection:
            all_routes_from_stop = connection.session.query(RouteStop).filter_by(stop_id=stop_id).all()
        return all_routes_from_stop

    def get_all_users_repo_():
        with DBConnection() as connection:
            all_users = connection.session.query(User).all()
        return all_users

    def add_new_user_(user):
        new_user = User(user.email, user.password)
        with DBConnection() as connection:
            connection.session.add(new_user)
            connection.session.commit()