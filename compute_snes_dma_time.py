#! /usr/bin/env python3

import os, sys

def printerr(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def sconcat(*args):
	ret = ""
	for arg in args:
		ret += str(arg)
	return ret

if (len(sys.argv) != 3):
	printerr(sconcat("Usage:  ", sys.argv[0], " width height"))
	exit(1)

class Blank:
	def __init__(self):
		pass

class Resolution:
	def __init__(self):
		self.__width = int(sys.argv[1])
		self.__height = int(sys.argv[2])
		pass

	def width(self):
		return self.__width

	def height(self):
		return self.__height


class Screen:
	def __init__(self):
		self.__constants = {"visible_width": 256, "total_width": 340,
			"visible_height": 224, "total_height": 262}

	def visible_width(self):
		return self.__constants["visible_width"]
	def total_width(self):
		return self.__constants["total_width"]
	def visible_height(self):
		return self.__constants["visible_height"]
	def total_height(self):
		return self.__constants["total_height"]

class NumCycles:
	def __init__(self):
		self.__constants = {"per_scanline": 1364, "per_wram_refresh": 40}
		self.__constants["available_per_scanline"] = (self.per_scanline()
			- self.per_wram_refresh())

	def per_scanline(self):
		return self.__constants["per_scanline"]
	def per_wram_refresh(self):
		return self.__constants["per_wram_refresh"]

	# Number of cycles available for doing things per scanline
	def available_per_scanline(self):
		return self.__constants["available_per_scanline"]

class NumBytes:
	def __init__(self, res):
		self.__res = res
		self.__screen = Screen()
		self.__num_cycles = NumCycles()

		self.__constants = {}
		self.__constants["per_frame"] = (self.__res.width()
			* self.__res.height())
		self.__constants["vram_used_for_tile_appearance"] \
			= (self.per_frame() * 1.5)
		self.__constants["to_upload_per_frame"] = (self.per_frame() / 2)
		self.__constants["uploadable_via_just_fblank_rows"] \
			= ((self.__screen.total_height() - self.__res.height())
			* self.__num_cycles.available_per_scanline() / 8)

		#num_pixels_of_uploadable_time_in_one_column = self.__res.width() \
		#	- 24

		num_pixels_uploadable_in_one_column \
			= (self.__screen.visible_width() - self.__res.width() - 24)
		column_height_no_overlap = self.__screen.visible_height() \
			- self.__res.height()
		num_bytes_uploadable_via_fblank_columns_no_overlap \
			= column_height_no_overlap \
			* num_pixels_uploadable_in_one_column
		self.__constants["uploadable_total"] \
			= self.uploadable_via_just_fblank_rows() \
			+ num_bytes_uploadable_via_fblank_columns_no_overlap

	def per_frame(self):
		return self.__constants["per_frame"]

	def vram_used_for_tile_appearance(self):
		return self.__constants["vram_used_for_tile_appearance"]
	def to_upload_per_frame(self):
		return self.__constants["to_upload_per_frame"]
	def uploadable_via_just_fblank_rows(self):
		return self.__constants["uploadable_via_just_fblank_rows"]
	def uploadable_total(self):
		return self.__constants["uploadable_total"]


class Compute:
	def __init__(self):
		self.__res = Resolution()


		self.__num_bytes = NumBytes(self.__res)

		self.__constants = {"horiz_pixels_per_tile" : 8,
			"vert_pixels_per_tile": 8}
		self.__constants["tiles_per_row"] = (self.res().width() / 8)
		self.__constants["tiles_per_column"] = (self.res().height() / 8)


	def horiz_pixels_per_tile(self):
		return self.__constants["horiz_pixels_per_tile"]
	def vert_pixels_per_tile(self):
		return self.__constants["vert_pixels_per_tile"]
	def tiles_per_row(self):
		return self.__constants["tiles_per_row"]
	def tiles_per_column(self):
		return self.__constants["tiles_per_column"]


	def res(self):
		return self.__res
	#def screen(self):
	#	return self.__screen
	#def num_cycles(self):
	#	return self.__num_cycles
	def num_bytes(self):
		return self.__num_bytes



compute = Compute()

#print(sconcat("res:  ", compute.res().width(), ", ",
#	compute.res().height()))
print(sconcat("num_bytes_per_frame():  ", compute.num_bytes().per_frame()))
print(sconcat("vram_used_for_tile_appearance():  ",
	compute.num_bytes().vram_used_for_tile_appearance()))
print(sconcat("num_bytes_to_upload_per_raw_frame():  ",
	compute.num_bytes().to_upload_per_frame()))
print(sconcat("num_bytes_uploadable_via_just_fblank_rows():  ",
	compute.num_bytes().uploadable_via_just_fblank_rows()))
print(sconcat("num_bytes_uploadable_total():  ",
	compute.num_bytes().uploadable_total()))
print(sconcat("tiles per row:  ", compute.tiles_per_row()))
print(sconcat("tiles per column:  ", compute.tiles_per_column()))
