from server import *
from server.db.home.autentication import Sign_In
from mongodb.get_the_last_id import last_id, get_custom_last_id

user_db = cluster["Auth"]
auth_collection_sign_in = user_db["Auth-Sign-In"]

subject_db = cluster["Subjects"]


class Teacher:
    def __init__(self, user_name, password, email, subject):
        try:
            self.user_name = user_name
            self.password = password
            self.email = email
            self.subject = subject
            self.subject_collection = subject_db[subject]
        except:
            self.user_name = "user_name"
            self.password = "password"
            self.email = "email"
            self.subject = "subject"
            self.subject_collection = "subject_db[subject]"

    def __repr__(self):
        return "Teacher"

    def add_teacher(self):
        try:
            si1 = Sign_In(
                user_name=self.user_name,
                password_or_email=self.password,
                role="Teacher",
            )
            si2 = Sign_In(
                user_name=self.user_name, password_or_email=self.email, role="Teacher"
            )
            results = [si1.check(), si2.check()]
            print(results)
            if results[0][0] is True or results[1][0] is True:
                return [False, "There is another teacher with the same info ! "]
            ids = last_id()
            auth_collection_sign_in.insert_one(
                {
                    "_id": ids,
                    "User Name": self.user_name,
                    "Password": self.password,
                    "Email": self.email,
                    "Role": "Teacher",
                    "Subject": self.subject,
                }
            )
            self.subject_collection.insert_one(
                {
                    "User Name": self.user_name,
                    "Password": self.password,
                    "Email": self.email,
                    "Role": "Teacher",
                    "Subject": self.subject,
                }
            )
            return [True, "New Teacher Created ! "]
        except:
            return False

    def delete_teacher(self, email, user_name):
        results = []
        for result in auth_collection_sign_in.find(
            {"User Name": user_name, "Email": email, "Role": "Teacher"}
        ):
            results.append(result)
        if results == []:
            return False
        print(results)
        for result_ in results:
            print(result_)
            auth_collection_sign_in.delete_one(result_)
        return True

    @staticmethod
    def get_data_of_teacher(user_name, email):
        results = []
        for result in auth_collection_sign_in.find(
            {"User Name": user_name, "Email": email, "Role": "Teacher"}
        ):
            results.append(result)
        if results == []:
            return [False, results]
        return [True, results]

    def update_teacher(self, new_info: dict, old_info: dict):
        si1 = Sign_In(
            user_name=new_info["User Name"],
            password_or_email=new_info["Password"],
            role=new_info["Role"],
        )
        si2 = Sign_In(
            user_name=new_info["User Name"],
            password_or_email=new_info["Email"],
            role=new_info["Role"],
        )
        results = [si1.check(), si2.check()]
        print(results[0][0])
        if results[0][0] is True or results[1][0] is True:
            return False
        results = []
        if new_info["Role"] == "Student":
            new = {
                "$set": {
                    "User Name": new_info["User Name"],
                    "Password": new_info["Password"],
                    "Email": new_info["Email"],
                    "Role": new_info["Role"],
                }
            }
            subject_collection = subject_db[old_info["Subject"]]
            subject_collection.delete_one(old_info)
        else:
            new = {
                "$set": {
                    "User Name": new_info["User Name"],
                    "Password": new_info["Password"],
                    "Email": new_info["Email"],
                    "Role": new_info["Role"],
                    "Subject": new_info["Subject"],
                }
            }
        print(old_info)
        print(new)
        try:
            auth_collection_sign_in.update_one(old_info[0], new)
        except:
            auth_collection_sign_in.update_one(old_info, new)
        return True

    @staticmethod
    def get_all_teachers():
        try:
            results_user = []
            for result_user in auth_collection_sign_in.find({"Role": "Teacher"}):
                results_user.append(result_user)
            return [results_user]
        except:
            return False

    @staticmethod
    def get_teachers(subject):
        try:
            results_user = []
            for result_user in auth_collection_sign_in.find(
                {"Role": "Teacher", "Subject": subject}
            ):
                results_user.append(result_user)
            return [results_user]
        except:
            return False


class Students:
    def __init__(self, user_name, password, email):
        try:
            self.user_name = user_name
            self.password = password
            self.email = email
        except:
            self.user_name = "user_name"
            self.password = "password"
            self.email = "email"

    def __repr__(self):
        return "Teacher"

    def add_student(self):
        si1 = Sign_In(
            user_name=self.user_name,
            password_or_email=self.password,
            role="Student",
        )
        si2 = Sign_In(
            user_name=self.user_name, password_or_email=self.email, role="Student"
        )
        results = [si1.check(), si2.check()]
        if results[0][0] is True or results[1][0] is True:
            return [
                False,
                "There is another student or a teacher or your  with the same info ! ",
            ]
        ids = last_id()
        auth_collection_sign_in.insert_one(
            {
                "_id": ids,
                "User Name": self.user_name,
                "Password": self.password,
                "Email": self.email,
                "Role": "Student",
            }
        )
        return [True, "New Student Created ! "]

    def delete_student(self, infos: list):
        for info in infos:
            try:
                auth_collection_sign_in.delete_one(info)
            except:
                pass
        return True

    def get_students(self):
        try:
            results = []
            for result in auth_collection_sign_in.find({"Role": "Student"}):
                results.append(result)
            return [True, results]
        except:
            return [False, ""]

    def update_student(self, new_info: dict, old_info: dict):
        si1 = Sign_In(
            user_name=new_info["User Name"],
            password_or_email=new_info["Password"],
            role=new_info["Role"],
        )
        si2 = Sign_In(
            user_name=new_info["User Name"],
            password_or_email=new_info["Email"],
            role=new_info["Role"],
        )
        results = [si1.check(), si2.check()]
        print(results)
        if results[0][0] is True or results[1][0] is True:
            return False
        print(old_info)
        old_info = old_info[0]
        if new_info["Role"] == "Student":
            new = {
                "$set": {
                    "_id": old_info["_id"],
                    "User Name": new_info["User Name"],
                    "Password": new_info["Password"],
                    "Email": new_info["Email"],
                    "Role": new_info["Role"],
                }
            }
            auth_collection_sign_in.update_one(old_info, new)
        else:
            new = {
                "$set": {
                    "_id": old_info["_id"],
                    "User Name": new_info["User Name"],
                    "Password": new_info["Password"],
                    "Email": new_info["Email"],
                    "Role": new_info["Role"],
                    "Subject": new_info["Subject"],
                }
            }
            subject_collection = subject_db[new_info["Subject"]]
            last_id_ = get_custom_last_id(db="Subjects", collection=new_info["Subject"])
            subject_collection.insert_one(
                {
                    "_id": last_id_,
                    "User Name": new_info["User Name"],
                    "Password": new_info["Password"],
                    "Email": new_info["Email"],
                    "Role": new_info["Role"],
                    "Subject": new_info["Subject"],
                }
            )
            auth_collection_sign_in.update_one(old_info, new)
        return True

    @staticmethod
    def get_data_of_student(user_name, email):
        auth_db = cluster["Auth"]
        auth_collection_sign_in = auth_db["Auth-Sign-In"]
        results = []
        for result in auth_collection_sign_in.find(
            {"User Name": user_name, "Email": email, "Role": "Student"}
        ):
            results.append(result)
        print(results)
        if results == []:
            return [False, results]
        return [True, results]
