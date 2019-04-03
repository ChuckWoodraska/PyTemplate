from typing import Callable
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db

class BaseModel(db.Model):
    __abstract__ = True

    @staticmethod
    def create(new_entry, commit=True):
        try:
            db.session.add(new_entry)
            if commit:
                db.session.commit()
            return new_entry.id
        except Exception as e:
            print("c", e)
            return False

    @classmethod
    def read(cls, id_) -> Callable[..., "BaseModel"]:
        return BaseModel.query.get(id_)

    def update(self):
        try:
            db.session.commit()
            return self.id
        except Exception as e:
            print("u", e)
            return False

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return self.id
        except Exception as e:
            print("d", e)
            return False

    @staticmethod
    def commit():
        db.session.commit()
        return True

    @staticmethod
    def object_dump(obj_name, obj_inst):
        def dig_deep(prop_value):
            dd_str = prop_value
            if (
                type(prop_value).__str__ is object.__str__
                and not isinstance(prop_value, str)
                and not isinstance(prop_value, dict)
            ):
                dd_str = BaseModel.object_dump(
                    prop_value.__class__.__name__, prop_value
                )
            return str(dd_str)

        obj_vars = sorted(
            [
                x
                for x in tuple(set(obj_inst.__dict__))
                if not x.startswith("__") and not x.startswith("_sa_instance_state")
            ]
        )
        return "{}({})".format(
            obj_name,
            ", ".join(
                [
                    "{}={}".format(var, dig_deep(getattr(obj_inst, var)))
                    for var in obj_vars
                ]
            ),
        )

    def __repr__(self):
        # return BaseModel.object_dump(self.__class__.__name__, self)
        obj_vars = sorted(
            [
                x
                for x in tuple(set(self.__dict__))
                if not x.startswith("__") and x != "_sa_instance_state"
            ]
        )
        return "{}({})".format(
            self.__class__.__name__,
            ", ".join(["{}={}".format(var, getattr(self, var)) for var in obj_vars]),
        )

    def serialize(self):
        fields = {}
        for key, value in self.__dict__.items():
            if not key.startswith("_") and key != "metadata":
                fields[key] = value
        return fields