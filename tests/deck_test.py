import os
import sys

# ensure project root is on sys.path so `src` can be imported when running tests directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.deck import Deck, Card, Suit


def test_build_deck_has_52_cards():
	d = Deck()
	assert d.remaining() == 52


def test_shuffle_deterministic_with_seed():
	d1 = Deck()
	d2 = Deck()
	d1.shuffle(seed=42)
	d2.shuffle(seed=42)
	# compare sequences
	seq1 = [str(c) for c in d1.peek(5)]
	# Rebuild and reshuffle in same way to compare
	d2 = Deck()
	d2.shuffle(seed=42)
	seq2 = [str(c) for c in d2.peek(5)]
	assert seq1 == seq2


def test_deal_reduces_count_and_returns_card():
	d = Deck()
	top = d.deal()
	assert isinstance(top, Card)
	assert d.remaining() == 51


def test_deal_many_and_order():
	d = Deck()
	dealt = d.deal(3)
	assert isinstance(dealt, list) and len(dealt) == 3
	assert d.remaining() == 49


def test_deal_too_many_raises():
	d = Deck()
	try:
		d.deal(53)
	except ValueError:
		pass
	else:
		raise AssertionError("Expected ValueError when dealing too many cards")


def test_burn_and_peek():
	d = Deck()
	before = d.remaining()
	top = d.peek(1)[0]
	d.burn(1)
	assert d.remaining() == before - 1
	# After burning top card, peek shows a different card now
	assert d.peek(1)[0] != top