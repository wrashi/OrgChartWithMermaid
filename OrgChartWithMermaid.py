import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd

# Set up SOLite db
engine = create_engine('sqlite:///:memory:', echo=False)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

emps = pd.read_csv("chinook.tsv", sep='\t')
emps.to_sql('employee', engine)

#	SQLAlchemy interface
class Employee(Base):
	__tablename__ = 'employee'
	
	EmployeeId = Column(Integer, primary_key=True)
	LastName = Column(String)
	FirstName = Column(String)
	Title = Column(String)
	ReportsTo = Column(Integer)
	Department = Column(String)
	Address	= Column(String)
	City = Column(String)
	
	def __repr__(self):
		return f"<Employee(FirstName={self.FirstName}, LastName={self.LastName})"

Base.metadata.create_all(engine)


class OrgChart(object):
	"""Initializes OrgChart class"""
	def __init__(self):
		super(OrgChart, self).__init__()
		self.display()
		
	def getUser(self, uid):
		"""Returns Employee instance corresponding to user id"""
		global session
		results = session.query(Employee).filter(Employee.EmployeeId == uid).one_or_none()
		return results
		
	def getUserIDs(self):
		"""Returns list of user ids for all users"""
		results = session.query(Employee.EmployeeId).order_by(Employee.EmployeeId).all()
		return results
		
	def getEmployeeCard(self, id):
		"""Returns a string representation of a user card for user id"""
		user = self.getUser(id)
		uid = getUIDString(id)
		title = user.Title.lower()
		if 'manager' in title:
			icon = "fa:fa-address-book"
			shapestart = "["
			shapeend = "]"
		elif 'staff' in title:
			icon = "fa:fa-user-circle"
			shapestart = "["
			shapeend = "]"
		else:
			icon = "fa:fa-user"
			shapestart = "{{"
			shapeend = "}}"
		response = f"""{uid}{shapestart}"`{icon} **{user.FirstName} {user.LastName}**
	{user.Title}
	*{user.City}*`"{shapeend} """
		return response

	def getUIDString(self, uid, withClass=False):
		"""Returns a user string for definition of a node or in the graph.
		Returns FirstName+ID for definitions.
		Returns FirstName+ID+:::City for nodes where :::City is a defined Mermaid style class"""
		user = self.getUser(uid)
		if not user:
			print("Found no user for UID", uid, user)
		fname = user.FirstName
		styleclass = user.City
		if withClass:
			uidstring = f"{fname}{uid}:::{styleclass}"
		else:
			uidstring = f"{fname}{uid}"
		return uidstring

	def processOrg(self):
		"""docstring for fname"""
		users = self.getUserIDs()
		managers = {}
		# Node definitions
		for x in users:
			x= x[0]
			uid = self.getUIDString(x) 
			user = self.getUser(x)
			print(self.getEmployeeCard(x))
			if user.ReportsTo and user.ReportsTo >= 1:
				ruid = int(user.ReportsTo)
				##  Add EmployeeId to Manager's list
				if ruid in managers:
					managers[ruid].append(int(x))
				else:
					managers[ruid] = [int(x)]
		print("\n")
		# Graph definition
		for m in managers:
			ruid = self.getUIDString(m, withClass=True) 
			manager = self.getUser(m)
			print(f"subgraph {manager.Department}")
			for e in managers[m]:
				uid = self.getUIDString(e, withClass=True)
				print(f"\t{ruid} --> {uid}")
			print("end")

	def display(self):
		print("""
```mermaid
%%{init: {"flowchart": {"curve": "stepAfter"}} }%%
flowchart TD
classDef Lethbridge fill:#FFCE54
classDef Calgary fill:#A0D468
classDef Edmonton fill:#8CC152
""")
		self.processOrg()
		print("```")

def main():
    oc = OrgChart()

if __name__ == '__main__':
    main()
