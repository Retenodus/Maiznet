########################################################################
# vim: fileencoding=utf-8 ts=8 noexpandtab :
#
# ~~~~ Maiznet.fr ~~~~
#
#  -> dhcp/utils.py
#
#
# Copyright 2011 Rémy Sanchez <remy.sanchez@hyperthese.net>
#
# This file is distributed under the terms of the WTFPL. For more
# informations, see http://sam.zoy.org/wtfpl/COPYING
########################################################################

# La classe BinString sert à manipuler simplement des chaînes bit par
# bit. Elle a été écrite pour JSZ (https://github.com/EquiNux/JSZ), et a
# été adaptée ici à la rache.

class BinString(object):
	"""
	Une classe d'aide pour aider à manipuler simplement des chaînes
	de bits.

	Issue du mini-projet `JSZ <https://github.com/EquiNux/JSZ>`_

	.. automethod:: __add__
	.. automethod:: __getitem__
	.. automethod:: __iadd__
	.. automethod:: __init__
	.. automethod:: __len__
	"""
	def __init__(self, value = ""):
		"""
		Initialise, la classe, avec éventuellement une valeur
		initiale à prendre en compte.
		"""
		self.bytes = bytearray()
		self.size = 0

		self.append(value)

	def append_bit(self, bit):
		"""
		Ajoute un bit à la fin de la chaîne
		"""
		if not isinstance(bit, (int, bool)):
			raise TypeError('Trying to append invalid bit')

		# Shall we extend the byte array ?
		if self.size % 8 == 0:
			self.bytes.append(0)

		octet = int(self.size / 8)
		offset = self.size % 8

		if bit:
			self.bytes[octet] = self.bytes[octet] | (128 >> offset)

		self.size += 1

	def append(self, other):
		"""
		Concatène la chaîne avec une autre chaîne binaire.
		"""
		if isinstance(other, str):
			for i in other:
				if i != '0' and i != '1':
					raise TypeError("Malformated string, must only contain 0 and 1")
				self.append_bit(i == '1')
		elif isinstance(other, BinString):
			self.bytes += other.bytes
			self.size += other.size
		elif isinstance(other, int):
			self.append_bit(other != 0)
		elif isinstance(other, bool):
			self.append_bit(other)
		else:
			raise TypeError('Unable to add this to the binary string')

	def __add__(self, other):
		"""
		Concatène les chaînes additionnées.
		"""
		out = BinString()
		out.bytes = self.bytes
		out.size = self.size

		out.append(other)

		return out

	def __iadd__(self, other):
		"""
		Raccourci pour ajouter une chaîne à la fin de celle ci.
		"""
		self.append(other)
		return self

	def get_bit(self, idx):
		"""
		Retourne un bit à un index précis.
		"""
		return self.bytes[int(idx / 8)] & (128 >> (idx % 8)) != 0

	def __len__(self):
		"""
		Retourne le nombre de bits dans la chaîne.
		"""
		return self.size

	def __getitem__(self, key):
		"""
		Accède à un bit en particulier.
		"""
		if not isinstance(key, int):
			raise TypeError("Indice must be int")

		if key >= self.size or key < 0:
			raise IndexError("Out of range")

		return self.get_bit(key)

	def bin(self):
		"""
		Retourne une représentation de la chaîne sous la forme
		d'une chaîne composée de 0 et de 1.
		"""
		out = ""
		for i in range(0, len(self)):
			if self[i]:
				out += "1"
			else:
				out += "0"

		return out

	def encode(self):
		"""
		Encode la chaîne dans un format spécial, fait pour être
		embarqué dans un commentaire de Javascript.
		"""
		from struct import pack
		out = bytearray()

		# number of trailing useless bits
		out.append((8 - len(self) % 8) % 8)

		# escape comment ends
		b = self.bytes
		places = []
		for i in range(1, len(b)):
			if b[i] == 47:
				if b[i - 1] == 42:
					b[i] = 42
					places.append(i)

		out += pack("H", len(places))
		for i in range(0, len(places)):
			out += pack("i", places[i])

		out += self.bytes
		return out

	def to_int(self):
		"""
		Converti les 4 premiers octets de la chaîne en entier.
		"""
		from struct import unpack
		return unpack('!I', str(self.bytes[0:4]))[0]

def tobinrep(val, size):
	"""
	Retourne la représentation binaire de l'entier val, avec un
	padding de 0 pour que la chaîne retournée fasse une longueur de
	size.

	Par exemple, tobinrep(1, 4) va retourner 0001.
	"""
	return bin(val)[2:].zfill(size)
