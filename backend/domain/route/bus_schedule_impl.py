import datetime

MEAN_BUS_VELOCITY = 4.7  # velocity in m/s

class BusScheduleImpl:

    def __init__(self, routes_repo, route_stop_repo, mock):
        self.routes_repo = routes_repo
        self.route_stop_repo = route_stop_repo
        self.mock = mock

    def get_travel_time_timedelta(self, stop_id, route_id):
        route_stop = self.route_stop_repo.return_route_stop_by_id(stop_id, route_id)
        if not route_stop.traveled_time: 
            travel_time = route_stop.traveled_dist / MEAN_BUS_VELOCITY
        else:
            travel_time = route_stop.traveled_time
        return datetime.timedelta(seconds=round(travel_time,2))

    def get_current_time_timedelta(self):
        if(self.mock):
            return datetime.timedelta(hours=9, minutes=0, seconds=0)
            
        cur_datetime = datetime.datetime.now()
        return datetime.timedelta(hours=cur_datetime.hour, 
                                minutes=cur_datetime.minute, 
                                seconds=round(cur_datetime.second,2))

    def get_timedelta_from_time_obj(self, time_obj):
        return datetime.timedelta(hours=time_obj.hour, 
                                minutes=time_obj.minute, 
                                seconds=round(time_obj.second,2))

    def get_arrival_time_impl(self, stop_id, route_id):
        travel_time_timedelta = self.get_travel_time_timedelta(stop_id, route_id)

        trip_list = self.routes_repo.return_trips_from_route(route_id)
        current_time = self.get_current_time_timedelta()
        best_arrival_time = None
        for trip in trip_list:
            time_obj = trip.departure_time
            departure_time = self.get_timedelta_from_time_obj(time_obj)
            arrival_time = departure_time + travel_time_timedelta
            if (arrival_time > current_time and (not best_arrival_time or arrival_time < best_arrival_time)):
                best_arrival_time = arrival_time
                
        return (str(best_arrival_time) or '')
    
    #def order_by_arrival_time_impl(self, routes_dict):
        # Converte o valor do dicionário de str para timedelta
        #timedelta_dict = dict( (x, [routes_dict[x][0], datetime.datetime.strptime(routes_dict[x][1],"%H:%M:%S.%f")] ) for x in routes_dict )
        # Ordena dicionário conforme timedelta
        #sorted_dict = dict( sorted( timedelta_dict.items(), key= lambda x: self.get_timedelta_from_time_obj(x[1][1]) ) )
        # Retorna dicionário convertendo timedelta para string novamente
        #return dict( (x, [sorted_dict[x][0], str(sorted_dict[x][1])[11:16] ] ) for x in sorted_dict )
