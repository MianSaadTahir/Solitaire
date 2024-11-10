import unittest
from cardDeck import CardDeck

class SolitaireTests(unittest.TestCase):

    def setUp(self):
        self.deck = CardDeck()
        self.deck.load_cards()
        self.deck.shuffle_cards()
        self.deck.load_piles((1100, 800))  

    def test_deck_contains_52_cards(self):
        self.assertEqual(len(self.deck.cards), 52, "The deck should have exactly 52 cards.")

    def test_pile_initialization(self):
        expected_pile_sizes = [1, 2, 3, 4, 5, 6, 7, 24]
        
        for i, pile in enumerate(self.deck.piles):
            self.assertEqual(len(pile.cards), expected_pile_sizes[i], f"Pile {i} should have {expected_pile_sizes[i]} cards.")

    def test_card_selection_from_pile(self):
        target_pile = self.deck.piles[6] 
        for card in target_pile.cards:
            card.face_up = True  
        click_position = (target_pile.cards[0].position[0] + 10, target_pile.cards[0].position[1] + 10)
        self.deck.handle_click(click_position)
        
        self.assertEqual(target_pile.cards, self.deck.selected_cards, "The selected cards should match the clicked pile's cards.")

if __name__ == '__main__':
    unittest.main()
