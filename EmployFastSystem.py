from datetime import datetime
from Mission import Mission
from Shuttle import Shuttle
from Administrator import Administrator
from Coordinator import Coordinator
from Candidate import Candidate
from Job import Job
from EmploymentRequirement import EmploymentRequirement
from CargoRequirement import CargoRequirement
from SelectionCriteria import SelectionCriteria


class EmployFastSystem:

    def __init__(self):
        self.__list_of_shuttles = self.read_shuttles()
        self.__list_of_users = self.read_users()
        self.__list_of_missions = self.read_missions()

    # read missions and relevant file, build mission list
    def read_missions(self):
        mission_data = self.read_data("data/missions.txt")
        job_data = self.read_data("data/jobs.txt")
        cargo_requirement = self.read_data("data/cargo_requirements.txt")
        selection_criteria = self.read_data("data/selection_criteria.txt")
        employment_requirements = self.read_data(
            "data/employment_requirements.txt")
        coordinator_data = self.read_data("data/users.txt")
        list_of_missions = []
        for m in mission_data:
            if m.strip() == "":
                continue
            data = [i.strip() for i in m.split(";")]
            mission_id = data[0]
            mission_name = data[1]
            description = data[2]
            country_of_origin = data[3]
            countries_allowed = data[4]
            launch_date = data[5]
            destination = data[6]
            duration = data[7]
            status = data[8]
            coordinator_id = data[9]
            shuttle_id = data[10]
            list_of_job = []
            # build job list for the mission
            for j in job_data:
                j_data = [a.strip() for a in j.split(";")]
                m_id = j_data[0]
                if mission_id == m_id:
                    list_of_job.append(Job(j_data[1], j_data[2]))
            list_of_cargo_requirements = []
            # build cargo requirement list for the mission
            for c in cargo_requirement:
                c_data = [q.strip() for q in c.split(";")]
                c_id = c_data[0]
                if mission_id == c_id:
                    list_of_cargo_requirements.append(
                        CargoRequirement(c_data[1], c_data[2], int(c_data[3])))
            list_of_selection_criteria = []
            # build selection criteria list for the mission
            for s in selection_criteria:
                s_data = [cr.strip() for cr in s.split(";")]
                s_id = s_data[0]
                if mission_id == s_id:
                    list_of_selection_criteria.append(SelectionCriteria(
                        int(s_data[1]) if s_data[1] else None, int(s_data[2]) if s_data[2] else None, eval(s_data[3]), eval(s_data[4])))
            list_of_employment_requirements = []
            # build employment requirement for the mission
            for e in employment_requirements:
                e_data = [emp.strip() for emp in e.split(";")]
                e_id = e_data[0]
                if mission_id == e_id:
                    list_of_employment_requirements.append(
                        EmploymentRequirement(e_data[1], int(e_data[2])))
            coordinator = None
            # get coordinator of the mission
            for co in coordinator_data:
                co_data = list(map(lambda x: x.strip(), co.split(";")))
                co_id = co_data[0]
                if co_id == coordinator_id:
                    coordinator = Coordinator(*co_data)
                    break

            mission = Mission(int(mission_id), mission_name, description, country_of_origin, countries_allowed,
                              datetime.strptime(
                                  launch_date, "%d/%m/%Y"), destination, int(duration), status,
                              list_of_job, list_of_cargo_requirements,
                              list_of_selection_criteria, list_of_employment_requirements,
                              coordinator)
            # assign shuttle if have
            if shuttle_id:
                for s in self.__list_of_shuttles:
                    if s.get_shuttle_id() == int(shuttle_id):
                        mission.set_shuttle(s)
                        break
            list_of_missions.append(mission)

        return list_of_missions

    # read user data and build the list of user
    def read_users(self):
        user_data = self.read_data("data/users.txt")
        list_of_users = []
        for u in user_data:
            if u.strip() == "":
                continue
            u_data = [use.strip() for use in u.split(";")]
            user_id = u_data[0]
            user_type = u_data[3]
            other_info = u_data[1:]
            user = None
            # build user based on user type
            if user_type == "Administrator":
                user = Administrator(int(user_id), *other_info)
            elif user_type == "Coordinator":
                user = Coordinator(int(user_id), *other_info)
            elif user_type == "Candidate":
                user = Candidate(int(user_id), *other_info[:4], datetime.strptime(other_info[4], "%d/%m/%Y"), *other_info[5:9],
                                 *[[y.strip() for y in x.split(',')] for x in other_info[9:14]], other_info[14],
                                 [y.strip() for y in other_info[15].split(',')])

            list_of_users.append(user)
        return list_of_users

    # read shuttle data and build the list of shuttle
    def read_shuttles(self):
        shuttle_data = self.read_data("data/shuttles.txt")
        list_of_shuttles = []
        for s in shuttle_data:
            if s.strip() == "":
                continue
            shut_data = [shu.strip() for shu in s.split(";")]
            shuttle_id = shut_data[0]
            shuttle_name = shut_data[1]
            manufacturing_year = shut_data[2]
            fuel_capacity = shut_data[3]
            passenger_capacity = shut_data[4]
            cargo_capacity = shut_data[5]
            travel_speed = shut_data[6]

            shuttle = Shuttle(int(shuttle_id), shuttle_name, int(manufacturing_year), int(fuel_capacity), int(passenger_capacity),
                          int(cargo_capacity), int(travel_speed))
            list_of_shuttles.append(shuttle)
        return list_of_shuttles

    # save the list of user into txt file
    def save_user_list(self):
        user_data = []
        for user in self.__list_of_users:
            user_type = user.get_user_type()
            # parse user to string based on the user type
            if user_type == "Administrator":
                user_data.append("; ".join([str(user.get_user_id()), user.get_user_name(), user.get_password(), user.get_user_type()]))
            elif user_type == "Coordinator":
                user_data.append("; ".join(
                    [str(user.get_user_id()), user.get_user_name(), user.get_password(), user.get_user_type(),
                     user.get_coordinator_name(), user.get_contact_info()]))
            elif user_type == "Candidate":
                user_data.append("; ".join(
                    [str(user.get_user_id()), user.get_user_name(), user.get_password(), user.get_user_type(),
                     user.get_candidate_name(), user.get_date_of_birth().strftime("%d/%m/%Y"), user.get_address(), user.get_nationality(),
                     user.get_identification_num(), user.get_gender(), ", ".join(user.get_allergies()),
                     ", ".join(user.get_food_preferences()), ", ".join(user.get_qualifications()), ", ".join(user.get_work_experience_years()),
                     ", ".join(user.get_occupation()), user.get_computer_skills(), ", ".join(user.get_languages_spoken())
                     ]))
        self.write_data("data/users.txt", user_data)

    # save list of mission into txt file
    def save_mission_list(self):
        mission_data = []
        job_data = []
        cargo_requirement_data = []
        selection_criteria_data = []
        employment_requirement_data = []
        for mission in self.__list_of_missions:
            mission_line = []
            mission_line.append(str(mission.get_mission_id()))
            mission_line.append(mission.get_mission_name())
            mission_line.append(mission.get_description())
            mission_line.append(mission.get_country_of_origin())
            mission_line.append(mission.get_countries_allowed())
            # parse datetime to string in dd/MM/yyyy format
            mission_line.append(mission.get_launch_date().strftime("%d/%m/%Y"))
            mission_line.append(mission.get_destination())
            mission_line.append(str(mission.get_duration()))
            mission_line.append(mission.get_status())
            mission_line.append(str(mission.get_coordinator().get_user_id()))
            mission_line.append(str(mission.get_shuttle().get_shuttle_id()) if mission.get_shuttle() else "")

            mission_data.append("; ".join(mission_line))
            for job in mission.get_list_of_job():
                job_data.append("; ".join(
                    [str(mission.get_mission_id()), job.get_job_name(), job.get_job_description()]))
            for cargo_requirement in mission.get_list_of_cargo_requirement():
                cargo_requirement_data.append("; ".join(
                    [str(mission.get_mission_id()), cargo_requirement.get_cargo_name(),
                     cargo_requirement.get_cargo_for(), str(cargo_requirement.get_quantity())]))
            for selection_criteria in mission.get_list_of_selection_criteria():
                # parse boolean to string
                selection_criteria_data.append("; ".join(
                    [str(mission.get_mission_id()), str(selection_criteria.get_min_age()) if selection_criteria.get_min_age() else "",
                     str(selection_criteria.get_max_age()) if selection_criteria.get_max_age() else "",
                     str(selection_criteria.get_health_record()), str(selection_criteria.get_criminal_record())]))
            for employment_requirement in mission.get_list_of_employment_requirement():
                employment_requirement_data.append("; ".join(
                    [str(mission.get_mission_id()), employment_requirement.get_title(), str(employment_requirement.get_required_number())]))

        self.write_data("data/missions.txt", mission_data)
        self.write_data("data/jobs.txt", job_data)
        self.write_data("data/cargo_requirements.txt", cargo_requirement_data)
        self.write_data("data/selection_criteria.txt", selection_criteria_data)
        self.write_data("data/employment_requirements.txt",
                        employment_requirement_data)

    # method to verify users and inputs
    def verify_user(self, username, password):
        for user in self.__list_of_users:
            if user.get_user_name() == username and user.get_password() == password:
                return user
        return None

    def get_mission(self, index, filter_func=None):
        if filter_func:
            missions = list(filter(filter_func, self.__list_of_missions))
            return missions[index]
        return self.__list_of_missions[index]

    def get_all_mission_name(self, filter_func=None):
        list_of_missions = self.__list_of_missions
        if filter_func:
            list_of_missions = filter(filter_func, list_of_missions)

        return list(map(lambda m: m.get_mission_name(), list_of_missions))

    # create a new mission with some default values
    def create_mission(self, mission_name="", description="", country_of_origin="", countries_allowed="", launch_date=None,
                       destination="", duration=None, status="Planning phase", list_of_job=[], list_cargo_requirement=[], list_selection_criteria=[],
                       list_employment_requirement=[], coordinator=None):
        mission_id = 1
        if self.__list_of_missions:
            mission_id = self.__list_of_missions[-1].get_mission_id() + 1
        mission = Mission(mission_id, mission_name, description, country_of_origin, countries_allowed, launch_date, destination,
                          duration, status, list_of_job, list_cargo_requirement, list_selection_criteria, list_employment_requirement, coordinator)
        return mission

    def add_new_mission(self, mission):
        self.__list_of_missions.append(mission)
        self.save_mission_list()

    def get_all_shuttle_name(self):
        return list(map(lambda s: s.get_shuttle_name(), self.__list_of_shuttles))

    def get_shuttle(self, index):
        return self.__list_of_shuttles[index]

    # create a new candidate with some default values
    def create_candidate_profile(self, user_name, password="", user_type="Candidate", candidate_name="", date_of_birth=None,
                                 address="", nationality="", identification_num="", gender="", allergies=[], food_preferences=[],
                                 qualifications=[], work_experience_years=[], occupation=[], computer_skills="", languages_spoken=[]):
        # check if the username is used
        for candidate in self.__list_of_users:
            if candidate.get_user_name() == user_name:
                return None

        user_id = 1
        if self.__list_of_users:
            user_id = self.__list_of_users[-1].get_user_id() + 1
        candidate = Candidate(user_id, user_name, password, user_type, candidate_name, date_of_birth, address, nationality, identification_num, gender,
                              allergies, food_preferences, qualifications, work_experience_years, occupation, computer_skills, languages_spoken)
        return candidate

    def add_new_user(self, user):
        self.__list_of_users.append(user)
        self.save_user_list()

    @staticmethod
    def assign_shuttle_to_mission(shuttle, mission):
        mission.set_shuttle(shuttle)

    @staticmethod
    def create_job(mission, job_name, job_description):
        job = Job(job_name, job_description)
        mission.get_list_of_job().append(job)

    @staticmethod
    def create_employment_requirement(mission, title, require_num):
        r = EmploymentRequirement(title, require_num)
        mission.get_list_of_employment_requirement().append(r)

    @staticmethod
    def create_cargo_requirement(mission, cargo_name, cargo_for, num):
        r = CargoRequirement(cargo_name, cargo_for, num)
        mission.get_list_of_cargo_requirement().append(r)

    @staticmethod
    def create_selection_criteria(mission, min_age=None, max_age=None, health_record=True, criminal_record=False):
        criteria = SelectionCriteria(
            min_age, max_age, health_record, criminal_record)
        mission.get_list_of_selection_criteria().append(criteria)

    # method to simulate get health record from third party
    @staticmethod
    def request_health_record(candidate):
        f = open("third-party/health_records.txt", "r")
        content_hr = f.readlines()
        for line in content_hr:
            data = line.split(",")
            if int(data[0].strip()) == candidate.get_user_id():
                return eval(data[1].strip())

    # method to simulate get criminal record from third party
    @staticmethod
    def request_criminal_record(candidate):
        f = open("third-party/criminal_records.txt", "r")
        content_cr = f.readlines()
        for line in content_cr:
            data = line.split(",")
            if int(data[0].strip()) == candidate.get_user_id():
                return eval(data[1].strip())

    @staticmethod
    def read_data(file_name):
        f = open(file_name, "r")
        return f.readlines()

    @staticmethod
    def write_data(file_name, data):
        f = open(file_name, "w")
        f.writelines([line + "\n" for line in data])
        f.close()
