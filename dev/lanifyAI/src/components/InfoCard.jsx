import { Card, CardContent } from "@/components/ui/card";
import PropTypes from 'prop-types';

export default function InfoCard({ imageUrl, title, subtitle }) {
    return (
        <Card className="w-80 shadow-sm hover:shadow-lg transition-shadow duration-300 ease-in border-0 group">
            <CardContent className="flex flex-col items-center p-6">
                <div className="w-16 h-16 rounded-full overflow-hidden flex items-center justify-center bg-gray-200">
                    {imageUrl && (
                        <img
                            src={imageUrl}
                            alt={title || "Card image"}
                            className="object-cover w-full h-full transition-transform duration-300 ease-in group-hover:scale-110"
                        />
                    )}
                </div>
                <h3 className="text-xl font-semibold mt-4">{title}</h3>
                <p className="text-sm text-gray-500">{subtitle}</p>
            </CardContent>
        </Card>
    );
}

InfoCard.propTypes = {
    imageUrl: PropTypes.string,
    title: PropTypes.string,
    subtitle: PropTypes.string,
};
