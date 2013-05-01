-- a file extension which Graffle supports for export
-- property new_extension : "pdf"
property export_extensions : {"pdf", "png"}
-- extra part of the file name
property export_filename : "_export"

on run {input}
	-- tell application "System Events"
	-- 	activate
	-- 	display dialog "Exporting " & input & "..."
	-- end tell
	log "Exporting " & input & " ..."
	set input_file to POSIX file input as alias
	repeat with new_extension in export_extensions
		set new_name to my rename(input_file, new_extension)
		log "Creating " & new_name
		set target_folder to my path_of_file(input_file)
		my process_item(input_file, new_name, target_folder)
	end repeat
end run

on path_of_file(this_file)
	tell application "Finder"
		set target_path to the folder of this_file
	end tell
	return the target_path
end path_of_file

-- this sub-routine just comes up with the new name
on rename(this_item, new_extension)
	tell application "Finder"
		set the file_name to the name of this_item
		set file_extension to the name extension of this_item
		if the file_extension is "" then
			set the trimmed_name to the file_name
		else
			set the trimmed_name to text 1 thru -((length of file_extension) + 2) of the file_name
		end if
		set target_name to (the trimmed_name & export_filename & "." & new_extension) as string
	end tell
	return the target_name
end rename

-- simple logging for debugging
on logme(log_string)
	log log_string
end logme

-- this sub-routine does the export 
on process_item(source_file, new_name, results_folder)
	set the source_item to the POSIX path of the source_file
	-- Make sure it can also handle file bundles
	if text -1 of source_item is "/" then
		set the source_item to text 1 through -2 of source_item
	end if
	set the target_path to (((results_folder as string) & new_name) as string)
	with timeout of 900 seconds
		tell application "OmniGraffle 5"
			-- save the current export settings so we can replace them later
			set oldAreaType to area type of current export settings
			set oldBorder to include border of current export settings
			
			-- here is where you set the export settings you want
			-- area type
			-- (all graphics/‌current canvas/‌entire document/‌manual region/‌selected graphics)
			set area type of current export settings to all graphics
			-- include border
			-- (Whether or not to include a border area around the exported graphics)
			set include border of current export settings to true
			-- draws background
			-- Draw the background canvas color (if false, leaves the background transparent during export).
			set draws background of current export settings to false
			
			-- open the file if it isn't already open
			set needToOpen to (count (documents whose path is source_item)) is 0
			if needToOpen then
				open source_file
			end if
			
			-- do the export
			set docsWithPath to documents whose path is source_item
			set theDoc to first item of docsWithPath
			save theDoc in file target_path
			
			-- if the file wasn't already open, close it again
			if needToOpen then
				close theDoc
			end if
			
			-- put the original export settings back
			set area type of current export settings to oldAreaType
			set include border of current export settings to oldBorder
		end tell
	end timeout
end process_item