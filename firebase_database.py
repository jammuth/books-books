import firebase_admin
from firebase_admin import credentials, firestore

class FirestoreDB:
	def __init__(self, config_path="./firebaseconfig.json", collection_name="kindle_books"):
		if not firebase_admin._apps:
			cred = credentials.Certificate(config_path)
			firebase_admin.initialize_app(cred)
		self._db = firestore.client()
		self.doc_ref = self._db.collection(collection_name).document("kindle_data")
		if not self.doc_ref.get().exists:
			self.doc_ref.set({})
		

	def add_item(self,item_dict):
		"""
		Add an item (dict) to the specified Firestore collection.
		Returns the document reference.
		"""
		# doc_ref = self._db.collection(collection_name).document()
		self.doc_ref.set(item_dict)
		print(self.doc_ref.id)
		return self.doc_ref.id