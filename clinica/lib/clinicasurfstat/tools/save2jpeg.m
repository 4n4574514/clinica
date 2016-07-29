%save2jpeg Saves a figure as a properly cropped jpg
%
%   save2jpeg(jpgFileName,handle,dpi)
%
%   - jpgFileName: Destination to write the jpg to.
%   - handle:  (optional) Handle of the figure to write to a jpg.  If
%              omitted, the current figure is used.  Note that handles
%              are typically the figure number.
%   - dpi: (optional) Integer value of dots per inch (DPI).  Sets
%          resolution of output jpg.  Note that 150 dpi is the Matlab
%          default and this function's default, but 600 dpi is typical for
%          production-quality.
%
%   Saves figure as a jpg with margins cropped to match the figure size.



function save2jpeg(jpgFileName,handle,dpi)

% Verify correct number of arguments
%narginchk(0,3);
error(nargchk(0,3,nargin));

% If no handle is provided, use the current figure as default
if nargin<1
    [fileName,pathName] = uiputfile('*.jpeg','Save to jpeg file:');
    if fileName == 0; return; end
    jpgFileName = [pathName,fileName];
end
if nargin<2
    handle = gcf;
end
if nargin<3
    dpi = 150;
end

% Backup previous settings
prePaperType = get(handle,'PaperType');
prePaperUnits = get(handle,'PaperUnits');
preUnits = get(handle,'Units');
prePaperPosition = get(handle,'PaperPosition');
prePaperSize = get(handle,'PaperSize');

% Make changing paper type possible
set(handle,'PaperType','<custom>');

% Set units to all be the same
set(handle,'PaperUnits','inches');
set(handle,'Units','inches');

% Set the page size and position to match the figure's dimensions
paperPosition = get(handle,'PaperPosition');
position = get(handle,'Position');
set(handle,'PaperPosition',[0,0,position(3:4)]);
set(handle,'PaperSize',position(3:4));
% set(handle, 'Fontsize', 2);

% Save the jpg (this is the same method used by "saveas")
print(handle,'-djpeg',jpgFileName,sprintf('-r%d',dpi))

% Restore the previous settings
set(handle,'PaperType',prePaperType);
set(handle,'PaperUnits',prePaperUnits);
set(handle,'Units',preUnits);
set(handle,'PaperPosition',prePaperPosition);
set(handle,'PaperSize',prePaperSize);
close all;
