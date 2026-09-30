from django.test import SimpleTestCase, TestCase

from .management.commands.import_docx_documents import (
	FAQ_SECTION_CATEGORIE,
	SEED_DIR,
	enrichir_faq_confirmee,
	extraire_faq,
)
from .staff_directory import STAFF_CONTACTS, creer_faq_contacts, synchroniser_contact_administration
from .models import Contact, Document, FAQ
from ai.services import retrieve


class ConfirmedFAQImportTests(SimpleTestCase):
	def _import_faq(self, filename, langue):
		source = extraire_faq(SEED_DIR / filename, FAQ_SECTION_CATEGORIE)
		return enrichir_faq_confirmee(source, langue)

	def _answer_containing(self, paires, fragment):
		return next(paire['reponse'] for paire in paires if fragment in paire['question'].lower())

	def test_arabic_location_and_registration_faq_are_enriched(self):
		paires = self._import_faq('05_FAQ_Bot_AR.docx', 'ar')

		location = self._answer_containing(paires, 'أين تقع المدرسة بالضبط')
		admission = self._answer_containing(paires, 'ما هي شروط القبول')
		dossier = self._answer_containing(paires, 'ما هي وثائق ملف الترشح')
		submission = self._answer_containing(paires, 'أين أودع ملف التسجيل')
		contact = self._answer_containing(paires, 'ما هو رقم هاتف المدرسة')

		self.assertIn('18.160797, -15.951593', location)
		self.assertIn('maps/dir/', location)
		self.assertIn('منصة «تكوين»', admission)
		self.assertIn('أربع صور شمسية حديثة', dossier)
		self.assertEqual(
			self._answer_containing(paires, 'ما مكونات ملف التسجيل'), dossier,
		)
		self.assertIn('مصلحة الشؤون الطلابية', submission)
		self.assertIn('36187111', contact)
		self.assertIn('46635996', contact)

	def test_french_location_and_registration_faq_are_enriched(self):
		paires = self._import_faq('06_FAQ_Bot_FR.docx', 'fr')

		location = self._answer_containing(paires, 'où se trouve exactement')
		admission = self._answer_containing(paires, 'quelles sont les conditions')
		dossier = self._answer_containing(paires, 'que contient le dossier')
		submission = self._answer_containing(paires, 'où déposer le dossier')
		contact = self._answer_containing(paires, 'quel est le téléphone')

		self.assertIn('18.160797, -15.951593', location)
		self.assertIn('maps/dir/', location)
		self.assertIn('Tekwin', admission)
		self.assertIn('quatre photos', dossier)
		self.assertIn('affaires estudiantines', submission)
		self.assertIn('36187111', contact)
		self.assertIn('46635996', contact)


class AdministrationContactSyncTests(TestCase):
	def test_contact_sync_is_idempotent(self):
		synchroniser_contact_administration()
		synchroniser_contact_administration()
		self.assertEqual(Contact.objects.count(), len(STAFF_CONTACTS) + 1)
		general_contact = Contact.objects.get(service='إدارة المدرسة')
		self.assertEqual(general_contact.telephone, '36187111 / 46635996')
		director = Contact.objects.get(service='Direction de l’EEFTP')
		self.assertIn('Mohamed Vall Yahya', director.role_associe)
		self.assertEqual(director.telephone, '36187111')
		self.assertEqual(director.email, 'mvyahya@mfpam.gov.mr')

	def test_contacts_have_arabic_and_french_faq_entries(self):
		arabic = creer_faq_contacts('ar')
		french = creer_faq_contacts('fr')

		self.assertGreater(len(arabic), len(STAFF_CONTACTS))
		self.assertGreater(len(french), len(STAFF_CONTACTS))
		self.assertTrue(any('مدير المدرسة' in pair['question'] for pair in arabic))
		self.assertTrue(any('Directeur de l’EEFTP' in pair['question'] for pair in french))
		self.assertTrue(any('intitulé à préciser' in pair['question'] for pair in french))


class ContactRetrievalTests(TestCase):
	def setUp(self):
		self.document = Document.objects.create(
			titre='Annuaire des contacts (test)',
			type_document='faq',
			langue='mixte',
			categorie_principale='contacts',
			statut_officialite='officiel_valide',
			niveau_confiance='haute',
			statut_activite='actif',
		)
		for langue in ('ar', 'fr'):
			for paire in creer_faq_contacts(langue):
				FAQ.objects.create(
					question=paire['question'],
					reponse=paire['reponse'],
					langue=langue,
					categorie=paire['categorie'],
					source_document=self.document,
					statut_activite='actif',
				)

	def test_arabic_role_variants_retrieve_the_requested_contact(self):
		for question, expected in (
			('من هو مدير المدرسة؟', 'Mohamed Vall Yahya'),
			('من مسؤول شعبة المناجم؟', 'Taleb Nouh'),
			('ما رقم رئيس شعبة RP؟', 'Azwine Mohamed Lemine El Hady'),
			('ما رقم رئيس مصلحة الدراسات والتدريبات؟', '26442641'),
		):
			with self.subTest(question=question):
				result = retrieve(question, langue='ar')
				self.assertTrue(result.passages)
				self.assertIn(expected, result.passages[0].contenu)

	def test_french_role_variants_retrieve_the_requested_contact(self):
		for question, expected in (
			('Qui est le directeur de l’EEFTP ?', 'Mohamed Vall Yahya'),
			('Qui dirige la filière mines ?', 'Taleb Nouh'),
			('Qui est Chef de filière RP ?', 'Azwine Mohamed Lemine El Hady'),
			('Quel est le numéro du Chef de service études et stages ?', '26442641'),
		):
			with self.subTest(question=question):
				result = retrieve(question, langue='fr')
				self.assertTrue(result.passages)
				self.assertIn(expected, result.passages[0].contenu)
