import csv

key = {
    # Trump
    "Trump": "Trump",
    "Donald Trump": "Trump",
    "President Trump": "Trump",
    "Ivanka Trump": "Ivanka Trump",
    "Eric Trump": "Eric Trump",
    "Don Jr": "Don Jr",
    "Donald Trump Jr": "Don Jr",
    "Melania Trump": "Melania Trump",
    
    # Epstein
    "Epstein": "Epstein",
    "Jeffrey Epstein": "Epstein",
    "Jeffery Epstein": "Epstein",
    "Jeff Epstein": "Epstein",
    
    # Maxwell
    "Maxwell": "Maxwell",
    "Ghislaine": "Maxwell",
    "Ghislaine Maxwell": "Maxwell",
    
    # Clinton
    "Clinton": "Clinton",
    "Bill Clinton": "Clinton",
    "President Clinton": "Clinton",
    "Hillary Clinton": "Hillary Clinton",
    "Hillary Rodham Clinton": "Hillary Clinton",
    
    # Other Politicians
    "Prince Andrew": "Prince Andrew",
    "Andrew Windsor": "Prince Andrew",
    "Duke of York": "Prince Andrew",
    "George Bush": "George Bush",
    "George W Bush": "George Bush",
    "George HW Bush": "George Bush",
    "Andrew Cuomo": "Andrew Cuomo",
    "Biden": "Biden",
    "Joe Biden": "Biden",
    "President Biden": "Biden",
    
    # Business/Tech Leaders
    "Bill Gates": "Bill Gates",
    "Elon Musk": "Elon Musk",
    "Les Wexner": "Les Wexner",
    "Leslie Wexner": "Les Wexner",
    "Larry Ellison": "Larry Ellison",
    
    # Legal/Associates
    "Dershowitz": "Dershowitz",
    "Alan Dershowitz": "Dershowitz",
    "Jean-Luc Brunel": "Jean-Luc Brunel",
    "Brunel": "Jean-Luc Brunel",
    "Jes Staley": "Jes Staley",
    "Bob Shapiro": "Bob Shapiro",
    "Robert Shapiro": "Bob Shapiro",
    
    # Victims/Witnesses
    "Virginia Giuffre": "Virginia Giuffre",
    "Virginia Roberts": "Virginia Giuffre",
    "Giuffre": "Virginia Giuffre",
    
    # Epstein Associates
    "Larry Visoski": "Larry Visoski",
    "Visoski": "Larry Visoski",
    "Lesley Groff": "Lesley Groff",
    "Groff": "Lesley Groff",
    "Sarah Kellen": "Sarah Kellen",
    "Kellen": "Sarah Kellen",
    "Nadia Marcinkova": "Nadia Marcinkova",
    "Marcinkova": "Nadia Marcinkova",
    
    # Other Names
    "Robin Leach": "Robin Leach",
    "Jamie Foxx": "Jamie Foxx",
    "Sammy Sosa": "Sammy Sosa",
    "Michael Moore": "Michael Moore",
    "Alexander Brothers": "Alexander Brothers",
    "Michael Jackson": "Michael Jackson",
    
    # Victims/Minors - Specific Terms
    "Underage Girl": "Girls",
    "Underage Girls": "Girls",
    "Minor Girl": "Girls",
    "Minor Girls": "Girls",
    "Teenage Girl": "Girls",
    "Teenage Girls": "Girls",
    "Young Girl": "Girls",
    "Young Girls": "Girls",
    "Young Woman": "Girls",
    "Young Women": "Girls",
    "Underaged": "Girls",
    "Minor": "Girls",
    "Minors": "Girls",
    "Girl": "Girls",
    
    # Victim Terms
    "Victim": "Victim",
    "Victims": "Victim",
    "Alleged Victim": "Victim",
    "Accuser": "Victim",
    "Accusers": "Victim",
    "Plaintiff": "Victim",
    "Plaintiffs": "Victim",
    "Complainant": "Victim",
    "Survivor": "Victim",
    "Survivors": "Victim",
    
    # Children/Babies
    "Child Victim": "Children",
    "Child Victims": "Children",
    "Child Abuse": "Abuse",
    "Child Exploitation": "Abuse",
    "Infant": "Babies",
    "Infants": "Babies",
    "Newborn": "Babies",
    "Newborn Baby": "Babies",
    
    # Locations - Specific
    "Little Saint James": "Little Saint James",
    "Little St James": "Little Saint James",
    "Epstein Island": "Little Saint James",
    "Private Island": "Little Saint James",
    "Zorro Ranch": "Zorro Ranch",
    "New Mexico Ranch": "Zorro Ranch",
    "Mar-A-Lago": "Mar-a-Lago",
    "Mar A Lago": "Mar-a-Lago",
    "Trump's Resort": "Mar-a-Lago",
    "Palm Beach Estate": "Palm Beach",
    "Palm Beach Mansion": "Palm Beach",
    "Manhattan Townhouse": "Manhattan",
    "Epstein's Townhouse": "Manhattan",
    "Upper East Side": "Manhattan",
    "Trump Plaza": "Trump Plaza",
    "Trump Tower": "Trump Tower",
    "Virgin Islands": "Virgin Islands",
    "US Virgin Islands": "Virgin Islands",
    "USVI": "Virgin Islands",
    "Rancho Palos Verdes": "Rancho Palos Verdes",
    
    # Travel - Specific
    "Lolita Express": "Flights",
    "Private Jet": "Flights",
    "Private Plane": "Flights",
    "Boeing 727": "Flights",
    "Flight Log": "Flights",
    "Flight Logs": "Flights",
    "Flight Manifest": "Flights",
    "Private Yacht": "Yacht",
    
    # Abuse Terms - Specific
    "Sexual Assault": "Assault",
    "Sexual Abuse": "Abuse",
    "Child Sexual Abuse": "Abuse",
    "Sexually Assaulted": "Assault",
    "Sexually Abused": "Abuse",
    "Rape": "Rape",
    "Raped": "Rape",
    "Gang Rape": "Rape",
    "Statutory Rape": "Rape",
    "Forced Sex": "Rape",
    "Non-Consensual": "Rape",
    "Assault": "Assault",
    "Assaulted": "Assault",
    "Molest": "Abuse",
    "Molested": "Abuse",
    "Molestation": "Abuse",
    "Penetration": "Abuse",
    "Penetrated": "Abuse",
    "Oral Sex": "Abuse",
    "Forced Oral": "Abuse",
    "Massage": "Massage",
    "Massages": "Massage",
    "Erotic Massage": "Massage",
    "Sexual Massage": "Massage",
    "Orgy": "Orgy",
    "Orgies": "Orgies",
    "Sex Party": "Orgy",
    "Sex Parties": "Orgy",
    
    # Trafficking - Specific
    "Sex Trafficking": "Trafficking",
    "Human Trafficking": "Trafficking",
    "Trafficked": "Trafficking",
    "Child Trafficking": "Trafficking",
    "Recruited": "Recruitment",
    "Groomed": "Recruitment",
    "Grooming": "Recruitment",
    "Procured": "Recruitment",
    "Sex Slave": "Trafficking",
    "Sex Slaves": "Trafficking",
    "Prostitution": "Trafficking",
    "Forced Prostitution": "Trafficking",
    
    # Violence - Specific
    "Ritual Abuse": "Ritual",
    "Ritualistic Abuse": "Ritual",
    "Satanic Ritual": "Ritual",
    "Sacrifice": "Ritual",
    "Human Sacrifice": "Ritual",
    "Ba'al": "Ba'al",
    "Baal": "Ba'al",
    "Moloch": "Moloch",
    "Molech": "Moloch",
    "Torture": "Torture",
    "Tortured": "Torture",
    "Murder": "Murder",
    "Murdered": "Murder",
    "Killed": "Murder",
    "Homicide": "Murder",
    "Strangled": "Murder",
    "Strangulation": "Murder",
    "Missing Person": "Missing",
    "Disappeared": "Missing",
    "Went Missing": "Missing",
    "Threat": "Threats",
    "Threatened": "Threats",
    "Death Threat": "Threats",
    "Blackmail": "Threats",
    "Blackmailed": "Threats",
    
    # Drugs - Specific
    "Drugged": "Drugs",
    "Drug-Induced": "Drugs",
    "Sedated": "Drugs",
    "Intoxicated": "Drugs",
    "Rohypnol": "Drugs",
    "Date Rape Drug": "Drugs",
    "Spiked Drink": "Drugs",
    "Cocaine": "Drugs",
    "Ecstasy": "Drugs",
    "MDMA": "Drugs",
    
    # Legal - Specific
    "Lawsuit": "Legal",
    "Lawsuits": "Legal",
    "Civil Suit": "Legal",
    "Criminal Case": "Legal",
    "Federal Case": "Legal",
    "Court Case": "Legal",
    "Deposition": "Legal",
    "Testimony": "Legal",
    "Testified": "Legal",
    "Settlement": "Settlement",
    "Settled": "Settlement",
    "Non-Disclosure Agreement": "Legal",
    "NDA": "Legal",
    "Confidentiality Agreement": "Legal",
    "Plea Deal": "Legal",
    "Indictment": "Legal",
    "Indicted": "Legal",
    
    # Organizations - Specific
    "Victoria's Secret": "Victoria's Secret",
    "VS Models": "Victoria's Secret",
    "Modeling Agency": "Modeling",
    "Model Agency": "Modeling",
    "Teen Models": "Modeling",
    "Modeling Scout": "Modeling",
    "Trump Modeling": "Modeling",
    "CIA": "CIA",
    "FBI": "FBI",
    "Federal Bureau": "FBI",
    "Mossad": "Israel",
    "Israeli Intelligence": "Israel",
    
    # Money - Specific (more context)
    "Hush Money": "Money",
    "Payoff": "Money",
    "Bribe": "Money",
    "Bribed": "Money",
    "Financial Settlement": "Settlement",
    "Wire Transfer": "Money",
    "Cash Payment": "Money",
    "Offshore Account": "Money",
    "Shell Company": "Money",
    
    # Financial Crisis
    "2008 Crisis": "2008 Crisis",
    "Financial Crisis": "Financial Crisis",
    "Market Crash": "Financial Crisis",
    "Economic Collapse": "Financial Crisis",
    "Trilateral Commission": "Trilateral Commission",
    
    # Crypto
    "Bitcoin": "Bitcoin",
    "Cryptocurrency": "Cryptocurrency",
    "Crypto Currency": "Cryptocurrency",
    "Blockchain": "Cryptocurrency",
    
    # Social/Political
    "Homeless": "Homeless",
    "Homelessness": "Homeless",
    "Abortion": "Abortion",
    "Gene Pool": "Gene Pool",
    "Eugenics": "Eugenics",
    "Eugenic": "Eugenics",
    "Genetic Selection": "Eugenics",
    
    # Conspiracy Terms
    "Pizza": "Pizza",
    "Pizzagate": "Pizza",
    "Hot Dog": "Pizza",
    "Wayfair": "Wayfair",
    "Wayfair Conspiracy": "Wayfair",
    "Calendar Girls": "Calendar Girls",
    "Muffin": "Muffin",
    
    # Easter Egg
    "Freddy Fazbear": "Freddy Fazbear",
    "Five Nights at Freddy's": "Freddy Fazbear",
}

# Write to CSV
with open('word_categories.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Word', 'Category'])
    for word, category in key.items():
        writer.writerow([word, category])

print("CSV created: word_categories.csv")