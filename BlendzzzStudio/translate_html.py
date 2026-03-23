# -*- coding: utf-8 -*-
"""Translate Bulgarian barbershop HTML to English. Run: python translate_html.py"""
import re
import sys

# Read from stdin or first arg
path = sys.argv[1] if len(sys.argv) > 1 else None
if path:
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
else:
    html = sys.stdin.read()

# Translations: Bulgarian -> English (order matters for overlapping strings)
TRANSLATIONS = [
    (r'<html lang="bg"', '<html lang="en"'),
    ('Професионално бръснарство Пловдив', 'Professional barbering Plovdiv'),
    ('Премиум мъжко обслужване в Пловдив. Две локации. Професионално бръснарство без компромис.', 'Premium men\'s grooming in Plovdiv. Two locations. Professional barbering without compromise.'),
    ('Към началото', 'To top'),
    ('За нас', 'About Us'),
    ('Локации', 'Locations'),
    ('Услуги', 'Services'),
    ('Екип', 'Team'),
    ('Отзиви', 'Reviews'),
    ('Фейсбук 1', 'Facebook 1'),
    ('Фейсбук 2', 'Facebook 2'),
    ('Запази час', 'Book appointment'),
    ('Меню', 'Menu'),
    ('Затвори', 'Close'),
    ('Избери локация', 'Select location'),
    ('Локация', 'Location'),
    ('Тракия', 'Trakia'),
    ('Център', 'Center'),
    ('Галерия', 'Gallery'),
    ('Контакти', 'Contact'),
    ('BASRI • Пловдив', 'BASRI • Plovdiv'),
    ('Тишина.', 'Silence.'),
    ('Прецизност.', 'Precision.'),
    ('Резултат.', 'Result.'),
    ('Две локации в Пловдив.', 'Two locations in Plovdiv.'),
    ('Професионално', 'Professional'),
    ('бръснарство без компромис.', 'barbering without compromise.'),
    ('Предимства', 'Why choose us'),
    ('Защо клиентите избират BASRI', 'Why clients choose BASRI'),
    ('15+ години опит • 2 локации • 4.9★ от Google', '15+ years experience • 2 locations • 4.9★ on Google'),
    ('Правим го както трябва от първия път', 'We get it right the first time'),
    ('Западно обучение. Резултатът личи веднага.', 'Western training. The result shows immediately.'),
    ('Обучени в Германия, Австрия и Швейцария—нашите бръснари разбират визията ти, дори когато не можеш да я обясниш с думи. Излизаш доволен, не „ами окей“.', 'Trained in Germany, Austria and Switzerland—our barbers understand your vision even when you can\'t put it into words. You leave satisfied, not "meh".'),
    ('Влизаш и излизаш без загуба на време', 'In and out without wasting time'),
    ('Онлайн час. Точно време. Готов си.', 'Online booking. On-time. You\'re done.'),
    ('Резервираш онлайн. Идваш навреме. Получаваш перфектна услуга. Продължаваш с деня си. Толкова просто.', 'Book online. Arrive on time. Get a perfect service. Get on with your day. That simple.'),
    ('Разговор или тишина — ти избираш.', 'Chat or silence—you choose.'),
    ('Нашият екип усеща какво ти трябва—съвет за стила, приятелски разговор или просто тишина и фокус. Ти задаваш тона.', 'Our team senses what you need—style advice, friendly chat or just peace and focus. You set the tone.'),
    ('Постоянство, на което разчиташ', 'Consistency you can rely on'),
    ('Всеки път — същото високо ниво.', 'Every time—the same high standard.'),
    ('Всяко посещение е като предишното—същата прецизност, същата грижа. Без лоши дни, без изненади. Знаеш какво получаваш.', 'Every visit is like the last—same precision, same care. No off days, no surprises. You know what you\'re getting.'),
    ('Стерилно. Нови консумативи. Всеки път.', 'Sterile. New consumables. Every time.'),
    ('Стерилизация на всеки инструмент. Нови консумативи за всеки клиент. Защото здравето на кожата ти не е преговорно.', 'Every tool sterilized. New consumables for every client. Because your skin health is non-negotiable.'),
    ('Две адреса, един стандарт', 'Two addresses, one standard'),
    ('Избери локация. Качеството е еднакво.', 'Pick your location. The quality is the same.'),
    ('Избери по-удобната локация. Качеството е идентично navсякъде.', 'Choose the more convenient location. The quality is identical everywhere.'),
    ('Избери локация и резервирай', 'Choose location and book'),
    ('Изберете Вашия салон', 'Choose your salon'),
    ('Изберете удобна локация • вижте цени, часове и контакти', 'Choose a convenient location • see prices, hours and contacts'),
    ('Салон 1 – Тракия', 'Salon 1 – Trakia'),
    ('Салон 2 – Център', 'Salon 2 – Center'),
    ('бул. „Шипка" 27 (кв. Капитан Бураго)', 'Shipka Blvd 27 (Captain Burago district)'),
    ('бул. „Пещерско шосе" 19', 'Peshtersko Shose Blvd 19'),
    ('отзива', 'reviews'),
    ('Пон–Съб:', 'Mon–Sat:'),
    ('Понеделник – Събота', 'Monday – Saturday'),
    ('Неделя', 'Sunday'),
    ('Избрана локация', 'Selected location'),
    ('Запази час тук', 'Book here'),
    ('Обади се', 'Call'),
    ('Работно време', 'Opening hours'),
    ('Стил, който говори сам', 'A style that speaks for itself'),
    ('Прецизно изпълнение • висок клас инструменти и козметика', 'Precise execution • high-end tools and cosmetics'),
    ('Избери локация, за да видиш актуални цени', 'Select a location to see current prices'),
    ('Фейд', 'Fade'),
    ('Подстригване', 'Haircut'),
    ('Оформяне на брада', 'Beard trim'),
    ('Кола маска', 'Clay mask'),
    ('Оформяне на вежди', 'Eyebrow shaping'),
    ('Бръснене на брада', 'Beard shave'),
    ('лв', 'BGN'),
    ('Промо', 'Promo'),
    ('Запази час сега', 'Book now'),
    ('Цените са ориентировъчни. Точните цени и налични часове са в онлайн резервацията.', 'Prices are indicative. Exact prices and available times are in the online booking.'),
    ('Кой ще се погрижи за теб', 'Who will take care of you'),
    ('Избери локация, за да видиш екипа.', 'Select a location to see the team.'),
    ('Бръснар', 'Barber'),
    ('Собственик • Главен бръснар', 'Owner • Head barber'),
    ('Екип – Тракия (4 бръснари)', 'Team – Trakia (4 barbers)'),
    ('Екип – Център (собственик + 1 бръснар)', 'Team – Center (owner + 1 barber)'),
    ('Запази час при нашия екип', 'Book with our team'),
    ('Реална работа. Реални кадри.', 'Real work. Real shots.'),
    ('Подстригвания, бради и атмосфера — без филтри.', 'Haircuts, beards and atmosphere—no filters.'),
    ('Покажи още', 'Show more'),
    ('Какво казват клиентите', 'What clients say'),
    ('Реални мнения от Google • общи за двете локации', 'Real reviews from Google • for both locations'),
    ('Предишен отзив', 'Previous review'),
    ('Следващ отзив', 'Next review'),
    ('Тишина, прецизност и безупречен резултат. Западен стандарт — в Пловдив.', 'Silence, precision and flawless result. Western standard—in Plovdiv.'),
    ('Страници', 'Pages'),
    ('Политика за поверителност', 'Privacy Policy'),
    ('Бисквитки', 'Cookies'),
    ('Общи условия', 'Terms and conditions'),
    ('Информация за компанията', 'Company information'),
    ('Всички права запазени.', 'All rights reserved.'),
    ('Професионално бръснарство. Без компромис в детайла.', 'Professional barbering. No compromise on detail.'),
    ('избери салон', 'select salon'),
    ('За цени/резервация по локация:', 'For prices/booking by location:'),
    ('Резервация –', 'Booking –'),
    ('Продължавате към онлайн резервация с налични часове и цени в реално време.', 'You will continue to online booking with available times and real-time prices.'),
    ('Продължи към резервация (скоро)', 'Continue to booking (coming soon)'),
    ('Смени локация', 'Change location'),
    ('Този сайт използва бисквитки за функционалност, аналитика и маркетинг. Можете да изберете кои бисквитки да приемете.', 'This site uses cookies for functionality, analytics and marketing. You can choose which cookies to accept.'),
    ('Приеми всички', 'Accept all'),
    ('Настройки', 'Settings'),
    ('Тук описвате събиране на данни, цели, правно основание, права на потребителите, трети страни, retention, контакт с администратора и DPO.', 'Here you describe data collection, purposes, legal basis, user rights, third parties, retention, and contact with the administrator and DPO.'),
    ('Сайтът използва строго необходими, аналитични и маркетингови бисквитки. Потребителят може да управлява съгласията си чрез банера за бисквитки.', 'The site uses strictly necessary, analytics and marketing cookies. Users can manage their consent via the cookie banner.'),
    ('Потребителите трябва да спазват правилата на сайта, ограниченията за отговорност, права върху интелектуална собственост, условия за е-комерс и процес за разрешаване на спорове.', 'Users must comply with the site\'s rules, liability limitations, intellectual property rights, e-commerce terms and dispute resolution process.'),
    ('Пълно юридическо наименование, адрес, UIC/BULSTAT, VAT номер, контакт e-mail и телефон, лиценз (ако е регламентирана индустрия).', 'Full legal name, address, UIC/BULSTAT, VAT number, contact email and phone, license (if a regulated industry).'),
    ('Отзиви', 'Reviews'),
    ('BASRI галерия', 'BASRI gallery'),
    ('BASRI снимка', 'BASRI photo'),
    ('Обади се на Barbershop BASRI', 'Call Barbershop BASRI'),
    ('(отваря се в нов таб)', '(opens in new tab)'),
    ('ул. „Шипка" 27, 4023 Пловдив (Капитан Бураго)', 'Shipka St 27, 4023 Plovdiv (Captain Burago)'),
    ('Пон–Съб: 09:00–19:00 • Нед: 09:00–17:00', 'Mon–Sat: 09:00–19:00 • Sun: 09:00–17:00'),
    ('бул. „Пещерско шосе" 19, 4002 Пловдив', 'Peshtersko Shose Blvd 19, 4002 Plovdiv'),
    ('Обади се на Barbershop BASRI – Тракия', 'Call Barbershop BASRI – Trakia'),
    ('Обади се на Barbershop BASRI – Център', 'Call Barbershop BASRI – Center'),
    ('Пон–Съб: 09:00 – 19:00, Неделя: 09:00 – 17:00', 'Mon–Sat: 09:00 – 19:00, Sun: 09:00 – 17:00'),
    ('Избери локация, за да видиш актуални цени', 'Select a location to see current prices'),
    ('Цени за локация: Тракия (Промо)', 'Prices for location: Trakia (Promo)'),
    ('Стандартни цени – Център', 'Standard prices – Center'),
    ('„Много приятно отношение. Всеки път излизам доволен."', '"Very pleasant service. I leave satisfied every time."'),
    ('„Хигиена и качество. Клиент съм от години — винаги на ниво."', '"Hygiene and quality. I\'ve been a client for years—always top notch."'),
    ('„Страхотен екип. 3 години клиент — без изненади, само резултат."', '"Great team. 3 years as a client—no surprises, just results."'),
    ('„Професионалисти. Коректно отношение и отлична услуга."', '"Professionals. Polite service and excellent work."'),
    ('„Много съм доволен — майсторска работа и топ обслужване."', '"Very satisfied—masterful work and great service."'),
]

for bg, en in TRANSLATIONS:
    html = html.replace(bg, en)

# Fix location names in JS
html = html.replace('name: "Салон 1 – Тракия"', 'name: "Salon 1 – Trakia"')
html = html.replace('shortName: "Тракия"', 'shortName: "Trakia"')
html = html.replace('shortName: "Център"', 'shortName: "Center"')
html = html.replace('name: "Салон 2 – Център"', 'name: "Salon 2 – Center"')

# Review names and texts in JS data array
html = html.replace('name: "Асен Пейчев"', 'name: "Asen Peychev"')
html = html.replace('text: "„Много приятно отношение. Всеки път излизам доволен.""', 'text: "\\"Very pleasant service. I leave satisfied every time.\\""')
html = html.replace('name: "Константин Костадинов"', 'name: "Konstantin Kostadinov"')
html = html.replace('text: "„Хигиена и качество. Клиент съм от години — винаги на ниво.""', 'text: "\\"Hygiene and quality. I\'ve been a client for years—always top notch.\\""')
html = html.replace('name: "Бранимир Бояджиев"', 'name: "Branimir Boyadzhiev"')
html = html.replace('text: "„Страхотен екип. 3 години клиент — без изненади, само резултат.""', 'text: "\\"Great team. 3 years as a client—no surprises, just results.\\""')
html = html.replace('name: "Величка Спасова"', 'name: "Velichka Spasova"')
html = html.replace('text: "„Професионалисти. Коректно отношение и отлична услуга.""', 'text: "\\"Professionals. Polite service and excellent work.\\""')
html = html.replace('name: "Али Мустафа"', 'name: "Ali Mustafa"')
html = html.replace('text: "„Много съм доволен — майсторска работа и топ обслужване.""', 'text: "\\"Very satisfied—masterful work and great service.\\""')

# Address in locations object
html = html.replace('address: \'ул. "Шипка" 27, 4023 Пловдив (Капитан Бураго)\'', 'address: \'Shipka St 27, 4023 Plovdiv (Captain Burago)\'')
html = html.replace('address: \'бул. "Пещерско шосе" 19, 4002 Пловдив (Център)\'', 'address: \'Peshtersko Shose Blvd 19, 4002 Plovdiv (Center)\'')

# aria-labels
html = html.replace('aria-label="Обади се на Barbershop BASRI – ${data.shortName}"', 'aria-label="Call Barbershop BASRI – ${data.shortName}"')

if path and path.endswith(".html"):
    out_path = path.replace(".html", "-en.html")
else:
    out_path = "barbershop-basri-en.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)
print("Written:", out_path)
