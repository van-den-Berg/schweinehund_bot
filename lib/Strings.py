import dataclasses
import random

from typing import Set, Dict

from models.Activity import Activity
from models.Group import Group


class Help:
    help_text = "this is a dummy text for the help section"
    avail_commands = "die folgenden Commands sind verfügbar: \n" \
                     "\t /join \tum der habbit tracking Funktion beizutreten\n" \
                     "\t /sport \twenn man sport gemacht hat\n" \
                     "\t /produktiv \twenn man seine Arbeitszeiten eingehalten hat\n" \
                     "\t /medienfrei \twenn man während der Arbeitszeiten keine unnötigen Medien konsumiert hat" \
                     "\t /rausgegangen \twenn man an dem Tag draußen unterwegs war" \
                     "\t /guterabend \twenn man an dem Abend nicht versackt ist"


def registration_succesfull_private(name: str) -> str:
    return f"Hallo und Willkommen {name}, wir freuen uns dass du hier bist!"


def registration_succesfull_group(name: str) -> str:
    return f"Woop Woop! Begrüßt {name} im Team!!"


class Errors:
    command_not_implemented: str = "Dieser Command ist zum aktuellen Zeitpunkt noch nicht implementiert."
    this_command_only_in_groups: str = "Dieser Command funktioniert nur in Gruppen."
    this_command_only_in_private_chat: str = "Dieser Command funktioniert nur im privaten Chat."

    user_not_registered_at_all: str = "Du bist leider in keiner Gruppe aktiv. Trete dem Habit-Tracking bei, indem du /join im Gruppenchat sendest."
    user_not_in_this_group: str = "Du nimmst zur Zeit nicht aktiv am Habit-Tracking dieser Gruppe teil. Um mitzumachen sende '/join' in diesen Chat."
    user_not_active_in_this_group: str = "Du hast das Habit Tracking in dieser Gruppe pausiert. Um den anderen wieder zu zeigen, wo der Hammer hängt, sende '/join'!"

    group_not_registered: str = "Das Habit-Tracking wurde in dieser Gruppe noch nicht aktiviert. Aktiviere es mit dem command '/registerGroup'."

    def group_not_allowed(group_id: str):
        return f"Diese Gruppe steht nicht auf der whitelist. Bitte kontaktiere die Administratoren. Die fehlende GruppenID ist {group_id}."


def init_no_data_at_location(path: str):
    return f"There is no file at provided path \n " \
           f"'data_json_path': '{path}'. \n " \
           f"An empty file for storing the data will be generated. \n " \
           f"If there should be a file with valid data, please check/change the config.json file."

class GroupManagement:

    paused_groups_successful = "Ich habe das Habit-Tracking in deinen aktiven Gruppen für dich pausiert. Wenn du wieder mit machen möchtest, dann schreibe einfach /weiter in den Chat."

    reactivated_groups_successful = "Willkommen zurück! Das Habit-Tracking wurde in allen deinen Gruppen wieder aktiviert."

    def paused_single_group_successful(group_name: str) -> str:
        last_str = "Wenn du wieder mit machen möchtest, dann schreibe einfach /weiter in den Chat."
        return f"Ich habe das Habit-Tracking in der Gruppe {group_name} für dich pausiert. {last_str}"

    def reactivated_single_group_successful(group_name: str) -> str:
        return f"Willkommen zurück! Das Habit-Tracking wurde in der Gruppe {group_name} wieder aktiviert."


class Registration:
    welcome_text = "Hey, schön dass du auch versuchst, deinen Arsch hoch zu bekommen! " \
                   "Damit alle wissen mit wem sie sich anlegen, fehlt noch dein Name. " \
                   "Mit diesem Namen wirst du in Zukunft von mir angesprochen und in Zusammenfassungen auftauchen. " \
                   "\n \n Wie darf ich dich nennen?"
    first_need_to_open_chat = "Damit du mitmachen kannst, musst du mich bei dir starten. " \
                              "Gehe dazu auf mein Profil und beginne einen Chat. " \
                              "Anschließend kannst du hierher zurückkommen und dich registrieren."
    already_registered = "Du bist bereits mit im Team!"

    class GroupRegistration:
        welcome_text = "Das Habit-Tracking für diese Gruppe wurde erfolgreich initialisiert. \n\nNutzer dieser Gruppe können nun mit '/join' am Habit-Tracking teilnehmen."
        already_registered = "Eure Gruppe nimmt bereits am Habit-Tracking teil. Nutzer dieser Gruppe können dem Tracking beitreten, indem sie '/join' in den Chat schreiben."

        def group_not_allowed(group_id: str):
            return f"Diese Gruppe steht nicht auf der whitelist. Bitte kontaktiere die Administratoren. Die fehlende GruppenID ist {group_id}."


@dataclasses.dataclass
class HabitStrings:

    yesterday_and_today_in_message_error = "Das eintragen von Erfolgen von gestern und heute innerhalb einer Nachricht wird nicht unterstützt. Bitte sende zwei einzelne Nachrichten."

    def added_to_groups(activity: Activity, group_ids: Set[str], groups: Dict[str, Group]) -> str:
        ret_str = f"Die Aktivität {activity} wurde erfolgreich in folgenden Gruppen hinzuefügt:\n"
        for group_id in group_ids:
            group_name: str = groups[group_id].group_name
            ret_str += f"{group_name},\n"
        return ret_str

    def activity_already_logged_for_today(activity: Activity, group: Group) -> str:
        ret_str = f"Das hättest du wohl gerne^^ {activity.name} ist für heute bereits in " \
                  f"Gruppe {group.group_name} eingetragen und wird nicht noch einmal gespeichert. Nicht cheaten ;-)"
        return ret_str

    def activity_already_logged_for_today_private(activity: Activity) -> str:
        ret_str = f"{activity.name} ist für heute bereits in allen deinen Gruppen" \
                  f" eingetragen und wird nicht noch einmal gespeichert. Nicht cheaten ;-)"
        return ret_str

    def get_habit_response(activity: Activity) -> str:
        if activity == Activity.SPORT:
            return random.choice(HabitStrings.sport)
        if activity == Activity.GOOD_EVENING:
            return random.choice(HabitStrings.evening)
        if activity == Activity.WENT_OUTSIDE:
            return random.choice(HabitStrings.outside)
        if activity == Activity.NO_MEDIA_DURING_WORK or activity == Activity.PRODUCTIVE_BY_10:
            return random.choice(HabitStrings.productive)

    sport = ["Nice, wir sind alle stolz auf dich!", "Wow, du bist ne krasse Sportskanone:-)",
             "Du zeigst uns allen wo der Hammer hängt!",
             "Das ballert!",
             "Cool dass du dich aufraffen konntest!",
             "Fühlst du wie gut dir der Sport getan hat?", "Krasser Bizeps!",
             "Entschuldigung können Sie mir sagen wo es zum Strand geht?",
             "Waschbrettbauch incomming!!!", "Komm und tanz mit mir einen kleinen Siegestanz!",
             "Du stehst im Telefonbuch unter T wie Tier ;-)",
             "HIT me baby, one more time!", "Sag mal weinst du oder ist das Schweiß der da von deiner Nase tropft?",
             "Run Forrest, Run!", "Komm, 5 schaffst du noch!",
             "I don't count my situps. I only start counting once it starts hurting. - Muhammad Ali",
             "I've failed over and over again in my life. And that is why I succeed. – Michael Jordan",
             "The only way to prove you are a good sport is to lose. – Ernie Banks",
             "There may be people that have more talent than you, but there's no excuse for anyone to work harder than you do. – Derek Jeter",
             "If you fail to prepare, you’re prepared to fail. – Mark Spitz",
             "The road to Easy Street goes through the sewer. – John Madden",
             "Stubbornness usually is considered a negative; but I think that trait has been a positive for me. - Cal Ripken, Jr.",
             "To uncover your true potential you must first find your own limits and then you have to have the courage to blow past them. – Picabo Street",
             "Never let your head hang down. Never give up and sit down and grieve. Find another way. – Satchel Paig",
             "Without self-discipline, success is impossible, period. – Lou Holtze",
             "There are no shortcuts to any place worth going. – Beverly Sills",
             "Kleine Idee für die nächste Sportsession: https://de.wikipedia.org/wiki/Roland_der_Furzer",
             "Dafür hast du dir ein Zuckerbonbon verdient. - Willst du ne Globoli?",
             "It's getting hot in here so take of all your clothes ;-)",
             "Schüttel dein Speck, schüttel dein Speck, baaaaa, bum badum badumdum..."]

    evening = ["Super und jetzt sei glücklich!",
               "Ich bin zwar nur ne Blechdose, aber immer für dich da wenn du mich brauchst. Wenn ich dir nicht antworte sag bitte Tim oder Paul Bescheid.",
               "Ich wünsche eine geruhsame Nacht!", "Träum was schönes!", "Was war das schönste an deinem Tag?",
               "Wein, Weib und Gesang, oderso...", "Sing doch noch mal probiers mal mit Gemütlichkeit",
               "Nimm dir heute mal 5 Minuten Zeit und versuche vor dem ins Bett gehen zu meditieren.",
               "Wann hast du das letzte Mal einen Mittagsschlaf gemacht?",
               "42.", "Such dir jemanden und veranstalte ein Candle Light Dinner zu zweit.",
               "Mach mal einen Wellness Abend. Wenn du nicht weißt wie das geht frag in die Gruppe!",
               "Worauf freust du dich gerade am meisten?",
               "Tu dir mal was gutes. Und plane es vorher, denn die Vorfreude ist die halbe Miete.",
               "Hast du was gesagt? - Spaß, ist notiert ;-)",
               "Tim ist der Größte und Paul ist der Hammer!!!",
               "Suche dir einen Spiegel und grinse 2 Minuten hinein! (Timer stellen!)",
               "Von wilden Blümlein die roten und Spechte sind Frühlingsboten.",
               "Antworte, sonst pflüge ich dich durch die Botanik, dass man dich für eine abgeknickte Tulpe hält. -Bud Spencer",
               "Chuck Norris isst keinen Honig, er kaut Bienen.", "Nahalla Maarsch! Oh sorry, ja ist notiert...",
               "Chuck Norris zerschneidet ein Messer mit einem Brot.",
               "Chuck Norris benutzt keine Kondome, denn es gibt nichts, was vor ihm schützen könnte.",
               "Chuck Norris ist so männlich, dass seine Brusthaare Haare haben.",
               "Chuck Norris liest keine Bücher. Er starrt sie so lange an, bis sie ihm freiwillig sagen was er wissen will.",
               "Wenn Chuck Norris ein Ei essen will, pellt er ein Huhn!",
               "Es gibt keine globale Erwärmung. Chuck Norris war kalt, also hat er die Sonne höher gedreht.",
               "Chuck Norris kennt die letzte Ziffer von Pi.",
               "Chuck Norris braucht weder Maus noch Tastatur. Er steckt einfach seinen rechten Zeigefinger in einen USB-Anschluss.",
               "Chuck Norris kann deine Gedanken mit einem Löffel verbiegen.",
               "Chuck Norris kann eine Drehtür zuschlagen."]

    outside = ["The wilderness holds answers to questions man has not yet learned to ask. – Nancy Newhall",
               "No matter the risks we take, we always consider the end to be too soon, even though in life, more than anything else, quality should be more important than quantity. – Alex Honnold",
               "Live the life you've dreamed. – Henry David Thoreau",
               "Life is full of beauty. Notice it. Notice the bumble bee, the small child, and the smiling faces. Smell the rain, and feel the wind. Live your life to the fullest potential, and fight for your dreams. – Ashley Smith",
               "The clearest way into the Universe is through a forest wilderness. – John Muir",
               "Now I see the secret of making the best person, it is to grow in the open air and to eat and sleep with the earth. – Walt Whitman",
               "All that is gold does not glitter, not all who wander are lost. – JRR Tolkien",
               "Live in the sunshine, swim in the sea, drink the wild air’s salubrity. – Ralph Waldo Emerson",
               "The joy of life comes from our encounters with new experiences, and hence there is no greater joy than to have an endlessly changing horizon, for each day to have a new and different sun.” – Alexander Supertramp Mccandless",
               "Real freedom lies in wildness, not in civilization. – Charles Lindbergh",
               "Just get out and do it. Just get out and do it. – Alexander Supertramp Mccandless",
               "The best thing one can do when it's raining is to let it rain. – Henry Longfellow",
               "Hiking's not for everyone. Notice the wilderness is mostly empty. – Sonja Yoerg",
               "An early - morning walk is a blessing for the whole day. – Henry David Thoreau",
               "Walking is a man’s best medicine. – Hippocrates",
               "Walking: the most ancient exercise and still the best modern exercise. – Carrie Latet",
               "Days of slow walking are very long: they make you live longer, because you have allowed every hour, every minute, every second to breathe, to deepen, instead of filling them up by straining the joints. – Frederic Gros",
               "Hiking and happiness go hand in hand or foot in boot. – Diane Spicer",
               "The best remedy for those who are afraid, lonely or unhappy is to go outside, somewhere where they can be quiet, alone with the heavens, nature and God. Because only then does one feel that all is as it should be and that God wishes to see people happy, amidst the simple beauty of nature. I firmly believe that nature brings solace in all troubles. – Anne Frank",
               "The sky is the daily bread of the eyes. – Ralph Waldo Emerson",
               "All truly great thoughts are conceived by walking. – Friedrich Nietzsche",
               "A journey of a thousand miles begins with a single step. – Lao-Tzu",
               "Hiking is not escapism; it’s realism. The people who choose to spend time outdoors are not running away from anything; we are returning to where we belong. – Jennifer Pharr Davis",
               "Returning home is the most difficult part of long-distance hiking. You have grown outside the puzzle and your piece no longer fits. – Cindy Ross",
               "If you are seeking creative ideas, go out walking. Angels whisper to a man when he goes for a walk. – Raymond Inmon",
               "After a day’s walk, everything has twice its usual value. – G.M.Trevelyan",
               "I took a walk in the woods and came out taller than the trees. – Henry David Thoreau"]

    productive = ["If you’re going through hell, keep going. – Winston Churchill",
                  "Eine Angewohnheit kann man nicht aus dem Fenster werfen. Man muss sie die Treppen hinunter prügeln! Stufe für Stufe. -Mark Twain",
                  "Es gibt nur einen Erfolg: Das Leben nach eigenen Vorstellungen leben zu können. -Christopher Morley",
                  "Müde macht nur die Arbeit die wir liegen lassen, nicht jene die wir tun.“ – Marie von Ebener-Eschenbach",
                  "Sogar der größte Experte war mal blutiger Anfänger! Also hab keine Angst davor den ersten Schritt zu machen!",
                  "Erfolg hat drei Buchstaben: TUN -Goethe",
                  "Das Gleiche lässt uns in Ruhe, aber der Widerspruch ist es, der uns produktiv macht. -Goethe",
                  "Krise ist ein produktiver Zustand. Mann muss ihm nur den Beigeschmack der Katastrophe nehmen. -Max Frisch",
                  "-p/2 +- sqrt(( p/2 ^2) - q)", "Im Magen von Blauwalen sind 35 Bar", "Sieben mal sieben ist feiner Sand."]
