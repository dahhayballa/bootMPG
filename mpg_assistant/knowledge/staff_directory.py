from knowledge.models import Contact

STAFF_CONTACTS = [
    {'service': 'Direction de l’EEFTP', 'role_fr': 'Directeur de l’EEFTP', 'role_ar': 'مدير المدرسة', 'name': 'Mohamed Vall Yahya', 'phone': '36187111', 'email': 'mvyahya@mfpam.gov.mr'},
    {'service': 'Études et stages', 'role_fr': 'Chef de service études et stages', 'role_ar': 'رئيس مصلحة الدراسات والتدريبات', 'name': 'Mahmoud Kalid Diakite', 'phone': '26442641', 'email': 'mahmouddiakite@yahoo.fr'},
    {'service': 'Ateliers et travaux', 'role_fr': 'Chef de service ateliers et travaux', 'role_ar': 'رئيس مصلحة الورشات والأشغال', 'name': 'Alion Bah', 'phone': '46523981', 'email': 'Aliyenebah@gmail.com'},
    {'service': 'Relations formation-emploi', 'role_fr': 'Chef de service relations formation-emploi', 'role_ar': 'رئيس مصلحة العلاقات بين التكوين والتشغيل', 'name': "Mohamed Nema Mohamed M'baye", 'phone': '46039233', 'email': 'mednema30@gmail.com'},
    {'service': 'Affaires financières et matériel', 'role_fr': 'Chef de service affaires financières et matériel', 'role_ar': 'رئيس مصلحة الشؤون المالية والمعدات', 'name': 'Fatimetou Med Nouh', 'phone': '36321128', 'email': ''},
    {'service': 'Surveillance générale', 'role_fr': 'Chef de service surveillance générale', 'role_ar': 'رئيس مصلحة المراقبة العامة', 'name': 'Sidi El Moktar Iyouh', 'phone': '0022246853808', 'email': 'Mdmocktar1970@gmail.com'},
    {'service': 'Filière électromécanique', 'role_fr': 'Chef de filière électromécanique', 'role_ar': 'رئيس شعبة الكهروميكانيك', 'name': 'El Khaliva Mohamed El Ghadhi', 'phone': '26350773 / 33350773', 'email': 'Khaliva16@gmail.com'},
    {'service': 'Filière PPG', 'role_fr': 'Chef de filière PPG', 'role_ar': 'رئيس شعبة الإنتاج النفطي والغازي (PPG)', 'name': 'Med Nouh', 'phone': '49887511', 'email': 'Kerimnouh5@gmail.com'},
    {'service': 'Filière RP', 'role_fr': 'Chef de filière RP', 'role_ar': 'رئيس شعبة التكرير والبتروكيمياء (RP)', 'name': 'Azwine Mohamed Lemine El Hady', 'phone': '36960660', 'email': 'zweinahady96@gmail.com'},
    {'service': 'Filière mines', 'role_fr': 'Chef de filière mines', 'role_ar': 'رئيس شعبة المناجم', 'name': 'Taleb Nouh', 'phone': '41959513', 'email': 'talebnouh90@gmail.com'},
    {'service': 'Filière (intitulé à préciser)', 'role_fr': 'Chef de filière (intitulé à préciser)', 'role_ar': 'رئيس شعبة (اسم الشعبة غير محدد في القائمة)', 'name': 'Mohammed Lemine Mohammed Abdellahi Ebou', 'phone': '33740474', 'email': 'ebbouuu@gmail.com'},
    {'service': 'Filière mécanique', 'role_fr': 'Chef de filière mécanique', 'role_ar': 'رئيس شعبة الميكانيكا', 'name': 'Oumar Sidi Ahmed', 'phone': '22238392 / 26909815', 'email': 'ouldsidahmedoumar@gmail.com'},
    {'service': 'Inclusion et handicap', 'role_fr': 'Référent inclusion / handicap', 'role_ar': 'مسؤول الإدماج ومرافقة ذوي الإعاقة', 'name': 'Eberahim Mohamed ebyaye', 'phone': '32585434', 'email': 'arbimarley@gmail.com'},
]


def synchroniser_contact_administration():
    Contact.objects.update_or_create(
        service='إدارة المدرسة',
        defaults={
            'role_associe': 'الإدارة',
            'telephone': '36187111 / 46635996',
            'statut_activite': 'actif',
        },
    )
    for item in STAFF_CONTACTS:
        Contact.objects.update_or_create(
            service=item['service'],
            defaults={
                'role_associe': f"{item['role_fr']} — {item['name']}",
                'telephone': item['phone'],
                'email': item['email'],
                'statut_activite': 'actif',
            },
        )


def creer_faq_contacts(langue: str) -> list[dict]:
    paires = []
    for item in STAFF_CONTACTS:
        if langue == 'ar':
            reponse = f"{item['role_ar']}: {item['name']}. الهاتف: {item['phone']}."
            if item['email']:
                reponse += f" البريد الإلكتروني: {item['email']}."
            sujet = item['role_ar'].removeprefix('رئيس ')
            service = item['service']
            questions = [
                f"من هو {item['role_ar']}؟",
                f"ما رقم {item['role_ar']}؟",
                f"كيف أتواصل مع {item['role_ar']}؟",
                f"من المسؤول عن {sujet}؟",
                f"ما رقم المسؤول عن {sujet}؟",
            ]
            if service.startswith('Filière '):
                questions.append(f"من مسؤول شعبة {sujet.removeprefix('شعبة ')}؟")
            elif item['service'] != 'Direction de l’EEFTP':
                questions.append(f"من المسؤول عن مصلحة {sujet.removeprefix('مصلحة ')}؟")
        else:
            reponse = f"{item['role_fr']} : {item['name']}. Téléphone : {item['phone']}."
            if item['email']:
                reponse += f" E-mail : {item['email']}."
            if item['role_fr'].startswith('Chef de service '):
                sujet = f"le service {item['role_fr'].removeprefix('Chef de service ')}"
            elif item['role_fr'].startswith('Chef de filière '):
                sujet = f"la filière {item['role_fr'].removeprefix('Chef de filière ')}"
            else:
                sujet = item['role_fr']
            questions = [
                f"Qui est {item['role_fr']} ?",
                f"Quel est le numéro du {item['role_fr']} ?",
                f"Comment contacter {item['role_fr']} ?",
                f"Qui dirige {sujet} ?",
            ]
        paires.extend(
            {'question': question, 'reponse': reponse, 'categorie': 'contacts'}
            for question in questions
        )
    return paires
